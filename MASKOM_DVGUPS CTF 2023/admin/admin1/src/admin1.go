package main

import (
	"bufio"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"os"
	"time"
)

func encode(msg string) string {
	return base64.StdEncoding.EncodeToString([]byte(msg))
}

func genString(length int) string {
	var s string
	r := make([]int, length)
	for _ = range r {
		s = s + genSymbol()
	}
	return s
}

func genSymbol() string {
	rand.Seed(time.Now().UnixNano())
	charset := "abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	c := charset[rand.Intn(len(charset))]
	return string(c)
}

func config(file string) (conf map[string]interface{}, err error) {
	jsonFile, err := os.Open(file)
	if err != nil {
		return
	}
	defer jsonFile.Close()
	byteValue, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		return
	}
	json.Unmarshal([]byte(byteValue), &conf)
	return
}

func getInput(input chan string) {
  in := bufio.NewReader(os.Stdin)
  result, err := in.ReadString('\n')
  if err != nil {
      log.Fatalf("Input error: %v", err)
  } else {
  	input <- result
  } 
}

func run(conf map[string]interface{}) bool {
	iter := int(conf["iterations"].(float64))
	length := int(conf["length"].(float64))
	timeout := int(conf["timeout"].(float64))
	input := make(chan string, 1)
	for i := 0; i < iter; i++ {
		s := genString(length)
		en := encode(s)
		fmt.Printf(`Iteration [%d/%d]
Give base64 decode string: %s
-> `, 
			i+1, iter, en,
		)
    go getInput(input)
		select {
      case i := <-input:
				i = i[:len(i)-1]
				log.Println(i, s, en)
				if i != s {
					return false
				} 
				//continue
      case <-time.After(time.Duration(timeout) * time.Second):
      	fmt.Println("Timed out.")
      	return false
    }
	}
	return true
}

const (
	confPath = "config.json"
)

func main() {
	conf, err := config(confPath)
	if err != nil {
		log.Fatalf("Config file open error: %v", err)
	}
	f, err := os.OpenFile(conf["logs"].(string), os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("Log file open error: %v", err)
	}
	defer f.Close()
	log.SetOutput(f)

	log.Println("Init session:", conf)
	if run(conf) == false {
		fmt.Println("FAIL!")
	} else {
		fmt.Println(conf["flag"])
	}
}
