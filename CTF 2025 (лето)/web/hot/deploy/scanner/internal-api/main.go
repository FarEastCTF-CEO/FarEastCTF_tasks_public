package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/golang-jwt/jwt/v5"
	_ "github.com/lib/pq"
)

var jwtSecret = os.Getenv("JWT_SECRET") // заменяется переменной окружения в docker

type Claims struct {
	Username string `json:"username"`
	Role     string `json:"role"`
	jwt.RegisteredClaims
}

func main() {
	dsn := os.Getenv("DATABASE_URL")
	if dsn == "" {
		log.Fatal("DATABASE_URL not set")
	}
	db, err := sql.Open("postgres", dsn)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	http.HandleFunc("/promote", func(w http.ResponseWriter, r *http.Request) {
		type promoteRequest struct {
			Username string `json:"username"`
			Role     string `json:"role"`
		}

		var req promoteRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid JSON", http.StatusBadRequest)
			return
		}

		if req.Username == "" || req.Role == "" {
			http.Error(w, "Missing username or role", http.StatusBadRequest)
			return
		}

		_, err := db.Exec("UPDATE users SET role=$1 WHERE username=$2", req.Role, req.Username)
		if err != nil {
			log.Printf("Failed to update role for user %s: %v", req.Username, err)
			http.Error(w, "Failed to update role", http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Role updated successfully"))
	})

	log.Println("internal-api running on :8000")
	http.ListenAndServe(":8000", nil)
}
