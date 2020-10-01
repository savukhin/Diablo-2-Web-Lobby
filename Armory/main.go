package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/nokka/d2s"
)

func sayhello(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Привет!")
}

func showChar(w http.ResponseWriter, r *http.Request) {
	path := r.URL.Path[1:]
	directory := "D:/PvPGN/Magic_Builder/release/var/charsave/"
	file, err := os.Open(directory + path)
	if err != nil {
		//log.Fatal("Error while opening .d2s file ", err)
		fmt.Fprintf(w, "Error while opening .d2s file ", err)
		return
	}

	defer file.Close()

	char, err := d2s.Parse(file)
	if err != nil {
		fmt.Fprintf(w, "Error:", err)
		return
	}

	// Prints character name and class.
	ans, err := json.Marshal(char)
	fmt.Fprintf(w, string(ans))

}

func favicon(w http.ResponseWriter, r *http.Request) {

}

func main() {
	http.HandleFunc("/favicon.ico", favicon)
	http.HandleFunc("/", showChar)           // Устанавливаем роутер
	err := http.ListenAndServe(":8001", nil) // устанавливаем порт веб-сервера
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
