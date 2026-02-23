package main

import (
	"log"
	"os"
	"path/filepath"
	. "scanner/routes"
	"time"
)

func Init() {
	go cleanupOldReports()
}
func cleanupOldReports() {
	ticker := time.NewTicker(5 * time.Second)
	for range ticker.C {
		files, err := filepath.Glob("/tmp/report-*")
		if err != nil {
			log.Printf("Error listing report dirs: %v", err)
			continue
		}
		for _, dir := range files {
			info, err := os.Stat(dir)
			if err != nil || !info.IsDir() {
				continue
			}
			if time.Since(info.ModTime()) > 10*time.Second {
				if err := os.RemoveAll(dir); err != nil {
					log.Printf("Failed to delete temp report dir %s: %v", dir, err)
				} else {
					log.Printf("Deleted old temp report dir: %s", dir)
				}
			}
		}
	}
}

// func secretRace() {
// 	go func() {
// 		createTicker := time.NewTicker(10 * time.Second)
// 		defer createTicker.Stop()

// 		for range createTicker.C {
// 			if err := os.WriteFile("/tmp/flag.txt", []byte(os.Getenv("FLAG_1")), 0644); err != nil {
// 				log.Printf("Error creating file: %v", err)
// 			} else {
// 				log.Println("Flag file created")
// 			}
// 		}
// 	}()

// 	cleanupTicker := time.NewTicker(2 * time.Second)
// 	defer cleanupTicker.Stop()

// 	for range cleanupTicker.C {
// 		files, err := filepath.Glob("/tmp/flag.txt")
// 		if err != nil {
// 			log.Printf("Error listing report dirs: %v", err)
// 			continue
// 		}
// 		for _, file := range files {
// 			info, err := os.Stat(file)
// 			if err != nil {
// 				log.Printf("Error stating file %s: %v", file, err)
// 				continue
// 			}
// 			if time.Since(info.ModTime()) > 3*time.Second {
// 				if err := os.Remove(file); err != nil {
// 					log.Printf("Failed to delete temp report file %s: %v", file, err)
// 				} else {
// 					log.Printf("Deleted old temp report file: %s", file)
// 				}
// 			}
// 		}
// 	}
// }

func main() {
	//go secretRace()
	go Init()
	InitRouter()
}
