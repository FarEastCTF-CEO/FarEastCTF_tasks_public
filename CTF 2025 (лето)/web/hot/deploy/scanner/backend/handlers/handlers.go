package handlers

import (
	"bytes"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	. "scanner/db"
	. "scanner/utils"

	"github.com/golang-jwt/jwt/v5"
	"github.com/gorilla/mux"
	"golang.org/x/crypto/bcrypt"
	"gopkg.in/yaml.v3"
)

type CurlTemplate struct {
	Method  string   `yaml:"method"`
	Headers []string `yaml:"headers"`
	Args    []string `yaml:"args"`
}

type OpenAPI struct {
	Servers []struct {
		URL string `yaml:"url"`
	} `yaml:"servers"`
	Paths map[string]map[string]Operation `yaml:"paths"`
}

type Operation struct {
	Parameters  []Parameter `yaml:"parameters"`
	RequestBody struct {
		Content map[string]struct {
			Schema struct {
				Properties map[string]Property `yaml:"properties"`
			} `yaml:"schema"`
		} `yaml:"content"`
	} `yaml:"requestBody"`
}

type Parameter struct {
	Name        string `yaml:"name"`
	In          string `yaml:"in"`
	Required    bool   `yaml:"required"`
	Description string `yaml:"description"`
	Schema      struct {
		Type    string `yaml:"type"`
		Default string `yaml:"default"`
		Example string `yaml:"example"`
	} `yaml:"schema"`
}

type Property struct {
	Type    string      `yaml:"type"`
	Example interface{} `yaml:"example"`
	Default interface{} `yaml:"default"`
}

type User struct {
	ID       int    `json:"id"`
	Username string `json:"username"`
	Password string `json:"password"`
	Role     string `json:"role"`
}
type RegisterUser struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

func LoginHandler(w http.ResponseWriter, r *http.Request) {
	var user RegisterUser
	_ = json.NewDecoder(r.Body).Decode(&user)

	row := DB.QueryRow("SELECT id, password, role FROM users WHERE username=$1", user.Username)
	var id int
	var hashedPwd, role string
	err := row.Scan(&id, &hashedPwd, &role)
	if err != nil || bcrypt.CompareHashAndPassword([]byte(hashedPwd), []byte(user.Password)) != nil {
		http.Error(w, "Invalid credentials", http.StatusUnauthorized)
		return
	}
	IssueToken(w, user.Username, role)
}

func RegisterHandler(w http.ResponseWriter, r *http.Request) {
	var user RegisterUser
	_ = json.NewDecoder(r.Body).Decode(&user)
	log.Println("REGISTER username =", user.Username)
	var exists bool
	err := DB.QueryRow("SELECT EXISTS(SELECT 1 FROM users WHERE username = $1)", user.Username).Scan(&exists)
	if err != nil {
		http.Error(w, "database error", http.StatusInternalServerError)
		return
	}
	if exists {
		http.Error(w, "username already taken", http.StatusConflict)
		return
	}
	hashedPwd, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
	if err != nil {
		http.Error(w, "Failed to register user", 500)
		return
	}

	_, err = DB.Exec("INSERT INTO users (username, password, role) VALUES ($1, $2, $3)", user.Username, string(hashedPwd), "user")
	fmt.Println(err)
	log.Println(err)
	if err != nil {
		http.Error(w, "Registration failed", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusCreated)
	w.Write([]byte("User registered"))
}

func ScanURLHandler(w http.ResponseWriter, r *http.Request) {
	type Req struct {
		URL string `json:"url"`
	}
	var req Req
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request", http.StatusBadRequest)
		return
	}

	// Получить пользователя из токена
	token, ok := TokenFromContext(r.Context())
	if !ok {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}
	claims := token.Claims.(jwt.MapClaims)
	username := claims["user"].(string)

	var userID int
	err := DB.QueryRow("SELECT id FROM users WHERE username=$1", username).Scan(&userID)
	if err != nil {
		http.Error(w, "User not found", 500)
		return
	}
	log.Printf("Start scan on url %s", req.URL)
	go runURLScan(userID, req.URL)

	w.Write([]byte("Scan started"))
}

func runURLScan(userID int, targetURL string) {
	files, _ := filepath.Glob("templates/*.yaml")

	for _, file := range files {
		data, err := os.ReadFile(file)
		if err != nil {
			log.Printf("Error reading template %s: %v", file, err)
			continue
		}

		var tmpl CurlTemplate
		if err := yaml.Unmarshal(data, &tmpl); err != nil {
			log.Printf("Invalid YAML %s: %v", file, err)
			continue
		}

		args := []string{"--request", tmpl.Method}
		for _, h := range tmpl.Headers {
			args = append(args, "--header", h)
		}
		args = append(args, tmpl.Args...)
		args = append(args, "--url", targetURL)

		u, err := url.Parse(targetURL)
		if err != nil {
			log.Printf("Invalid target URL: %v", err)
			continue
		}
		paramsJSON, _ := json.Marshal(tmpl.Args)
		var scanID int
		err = DB.QueryRow(`
			INSERT INTO scans (user_id, method, path, host, params, response, status)
			VALUES ($1, $2, $3, $4, $5, '', 'running') RETURNING id
		`, userID, tmpl.Method, u.Path, u.Host, paramsJSON).Scan(&scanID)
		if err != nil {
			log.Printf("DB insert error: %v", err)
			continue
		}
		log.Printf("Start curl command %v", args)
		out, err := exec.Command("curl", args...).CombinedOutput()
		if err != nil {
			log.Printf("curl failed: %v", err)
			_, _ = DB.Exec("UPDATE scans SET response=$1, status='error' WHERE id=$2", string(out), scanID)
			continue
		}

		_, err = DB.Exec("UPDATE scans SET response=$1, status='done' WHERE id=$2", string(out), scanID)
		if err != nil {
			log.Printf("DB update error: %v", err)
		}
	}
}

func ScanSwaggerHandler(w http.ResponseWriter, r *http.Request) {
	r.ParseMultipartForm(10 << 20)
	file, _, err := r.FormFile("swagger")
	if err != nil {
		http.Error(w, "Invalid file", 400)
		return
	}
	defer file.Close()

	var spec OpenAPI
	decoder := yaml.NewDecoder(file)
	if err := decoder.Decode(&spec); err != nil {
		http.Error(w, "Failed to parse swagger", 500)
		return
	}

	token, ok := TokenFromContext(r.Context())
	if !ok {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}
	claims := token.Claims.(jwt.MapClaims)
	username := claims["user"].(string)
	var userID int
	err1 := DB.QueryRow("SELECT id FROM users WHERE username=$1", username).Scan(&userID)
	if err1 != nil {
		http.Error(w, "User not found", 500)
		return
	}

	server := "http://localhost"
	if len(spec.Servers) > 0 {
		server = spec.Servers[0].URL
	}

	for path, methods := range spec.Paths {
		for method, meta := range methods {
			go func(method string, meta Operation, path string) {
				url := fmt.Sprintf("%s%s", server, path)
				args := []string{"-X", strings.ToUpper(method)}

				queryParams := []string{}
				var bodyParams []string

				for _, param := range meta.Parameters {
					value := "test"
					if param.Schema.Example != "" {
						value = param.Schema.Example
					} else if param.Schema.Default != "" {
						value = param.Schema.Default
					}

					switch param.In {
					case "query":
						queryParams = append(queryParams, fmt.Sprintf("%s=%s", param.Name, value))
					case "header":
						args = append(args, "-H", fmt.Sprintf("%s: %s", param.Name, value))
					case "path":
						url = strings.Replace(url, fmt.Sprintf("{%s}", param.Name), value, 1)
					case "cookie":
						args = append(args, "--cookie", fmt.Sprintf("%s=%s", param.Name, value))
					}
				}

				if len(queryParams) > 0 {
					url += "?" + strings.Join(queryParams, "&")
				}

				if len(meta.RequestBody.Content) > 0 {
					if content, ok := meta.RequestBody.Content["application/json"]; ok {
						for propName, prop := range content.Schema.Properties {
							val := "test"
							if prop.Example != nil {
								val = fmt.Sprintf("%v", prop.Example)
							} else if prop.Default != nil {
								val = fmt.Sprintf("%v", prop.Default)
							}
							bodyParams = append(bodyParams, fmt.Sprintf("\"%s\": \"%s\"", propName, val))
						}
					}
				}

				if len(bodyParams) > 0 {
					jsonBody := fmt.Sprintf("{%s}", strings.Join(bodyParams, ", "))
					args = append(args, "-H", "Content-Type: application/json", "--data", jsonBody)
				}

				args = append(args, url)
				paramsString, _ := json.Marshal(args)

				var scanID int
				err := DB.QueryRow(`
					INSERT INTO scans (user_id, method, path, host, params, response, status)
					VALUES ($1, $2, $3, $4, $5, '', 'running') RETURNING id
				`, userID, strings.ToUpper(method), path, server, paramsString).Scan(&scanID)
				if err != nil {
					log.Printf("Failed to insert scan: %v", err)
					return
				}

				cmd := exec.Command("curl", args...)
				output, err := cmd.CombinedOutput()
				status := "done"
				if err != nil {
					status = "error"
					log.Printf("Scan error [%s]: %v", url, err)
				}

				_, err = DB.Exec(`
					UPDATE scans SET response = $1, status = $2 WHERE id = $3
				`, string(output), status, scanID)
				if err != nil {
					log.Printf("Failed to update scan: %v", err)
				}
			}(method, meta, path)
		}
	}

	w.Write([]byte("Swagger scan started"))
}

func GetUsersHandler(w http.ResponseWriter, r *http.Request) {
	rows, err := DB.Query("SELECT id, username, role FROM users ORDER BY id")
	if err != nil {
		http.Error(w, "DB error", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var users []User
	for rows.Next() {
		var u User
		if err := rows.Scan(&u.ID, &u.Username, &u.Role); err == nil {
			users = append(users, u)
		}
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(users)
}

func UpdateUserRoleHandler(w http.ResponseWriter, r *http.Request) {
	id := mux.Vars(r)["id"]
	type payload struct {
		Role string `json:"role"`
	}
	var p payload
	if err := json.NewDecoder(r.Body).Decode(&p); err != nil {
		http.Error(w, "Invalid body", http.StatusBadRequest)
		return
	}
	if p.Role != "admin" && p.Role != "user" {
		http.Error(w, "Invalid role", http.StatusBadRequest)
		return
	}
	_, err := DB.Exec("UPDATE users SET role=$1 WHERE id=$2", p.Role, id)
	if err != nil {
		http.Error(w, "Update failed", http.StatusInternalServerError)
		return
	}
	w.Write([]byte("Role updated"))
}

func SecretHandler(w http.ResponseWriter, r *http.Request) {
	data, err := os.ReadFile("secret.txt")
	if err != nil {
		http.Error(w, "not found", 404)
		return
	}
	json.NewEncoder(w).Encode(map[string]string{"secret": string(data)})
}

func GetResultHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	token, ok := TokenFromContext(r.Context())
	if !ok {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}
	claims := token.Claims.(jwt.MapClaims)
	username := claims["user"].(string)

	row := DB.QueryRow("SELECT id, method, url, response, created_at FROM scans WHERE id=$1 AND username=$2", id, username)

	type Scan struct {
		ID        int       `json:"id"`
		Method    string    `json:"method"`
		URL       string    `json:"url"`
		Response  string    `json:"response"`
		CreatedAt time.Time `json:"created_at"`
	}
	var s Scan

	err := row.Scan(&s.ID, &s.Method, &s.URL, &s.Response, &s.CreatedAt)
	if err != nil {
		http.Error(w, "Scan not found or access denied", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(s)
}

func GetScansHandler(w http.ResponseWriter, r *http.Request) {
	token, ok := TokenFromContext(r.Context())
	if !ok {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}
	claims := token.Claims.(jwt.MapClaims)
	username := claims["user"].(string)

	query := `
		SELECT 
			s.id, s.method, s.host || s.path AS url, s.params, s.response, s.status, s.created_at
		FROM scans s
		JOIN users u ON s.user_id = u.id
		WHERE u.username = $1
		ORDER BY s.created_at DESC;
	`
	rows, err := DB.Query(query, username)
	if err != nil {
		http.Error(w, "Database error", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	type Scan struct {
		ID        int       `json:"id"`
		Method    string    `json:"method"`
		URL       string    `json:"url"`
		Params    string    `json:"params"`
		Response  string    `json:"response"`
		Status    string    `json:"status"`
		CreatedAt time.Time `json:"created_at"`
	}

	var scans []Scan
	for rows.Next() {
		var s Scan
		err := rows.Scan(&s.ID, &s.Method, &s.URL, &s.Params, &s.Response, &s.Status, &s.CreatedAt)
		if err != nil {
			continue
		}
		scans = append(scans, s)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(scans)
}

func GenerateReportHandler(w http.ResponseWriter, r *http.Request) {
	type Req struct {
		Host string `json:"host"`
		HTML string `json:"html"`
	}
	var req Req
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	buf := make([]byte, 8)
	rand.Read(buf)
	suffix := hex.EncodeToString(buf)
	dir := "/tmp/report-" + suffix
	os.MkdirAll(dir, 0700)

	htmlPath := filepath.Join(dir, "index.html")
	pdfPath := filepath.Join(dir, "report.pdf")

	if err := os.WriteFile(htmlPath, []byte(req.HTML), 0644); err != nil {
		http.Error(w, "Failed to write HTML", 500)
		return
	}

	go func() {
		cmd := exec.Command("curl",
			"-F", fmt.Sprintf("files=@%s;type=text/html", htmlPath),
			"-F", "index.html=index.html",
			"http://gotenberg:3000/forms/chromium/convert/html")
		var out bytes.Buffer
		cmd.Stdout = &out
		cmd.Stderr = &out
		if err := cmd.Run(); err != nil {
			log.Printf("gotenberg error: %v", err)
			return
		}
		os.WriteFile(pdfPath, out.Bytes(), 0644)
	}()

	link := fmt.Sprintf("/reports/report-%s/report.pdf", suffix)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"url": link,
	})
}
