package router

import (
	"log"
	"net/http"

	. "scanner/handlers"
	. "scanner/utils"

	"github.com/gorilla/mux"
)

func InitRouter() {
	r := mux.NewRouter()
	r.HandleFunc("/login", LoginHandler).Methods("POST")
	r.HandleFunc("/register", RegisterHandler).Methods("POST")
	r.PathPrefix("/reports/").Handler(http.StripPrefix("/reports/", http.FileServer(http.Dir("/tmp"))))
	api := r.PathPrefix("/api").Subrouter()
	api.Use(AuthMiddleware)
	api.HandleFunc("/generate-report", GenerateReportHandler).Methods("POST")
	api.HandleFunc("/scan/url", ScanURLHandler).Methods("POST")
	api.HandleFunc("/scan/swagger", ScanSwaggerHandler).Methods("POST")
	api.HandleFunc("/scans", GetScansHandler).Methods("GET")
	api.HandleFunc("/result/{id}", GetResultHandler).Methods("GET")
	api.HandleFunc("/users", AdminOnly(GetUsersHandler)).Methods("GET")
	api.HandleFunc("/user/{id}/role", AdminOnly(UpdateUserRoleHandler)).Methods("POST")
	api.HandleFunc("/secret", AdminOnly(SecretHandler)).Methods("GET")
	handler := CorsMiddleware(r)
	log.Println("Server running on :8080")
	http.ListenAndServe(":8080", handler)
}
