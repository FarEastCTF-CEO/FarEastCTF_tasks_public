package database

import (
	"database/sql"
	"log"
	"os"

	_ "github.com/lib/pq"
)

var (
	DB = InitDB(os.Getenv("DATABASE_URL"))
)

func InitDB(dataSourceName string) *sql.DB {
	db, err := sql.Open("postgres", dataSourceName)
	if err != nil {
		log.Fatal("cannot connect to database:", err)
	}

	schema := `
	CREATE TABLE IF NOT EXISTS users (
		id SERIAL PRIMARY KEY,
		username TEXT UNIQUE NOT NULL,
		password TEXT NOT NULL,
		role TEXT NOT NULL DEFAULT 'user'
	);

	CREATE TABLE IF NOT EXISTS scans (
		id SERIAL PRIMARY KEY,
		user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
		method TEXT NOT NULL,
		path TEXT NOT NULL,
		host TEXT NOT NULL,
		response TEXT DEFAULT '',
		params JSONB,
		status TEXT DEFAULT 'pending',
		created_at TIMESTAMP DEFAULT now()
	);
	`

	_, err = db.Exec(schema)
	if err != nil {
		log.Fatal("failed to initialize schema:", err)
	}

	return db
}
