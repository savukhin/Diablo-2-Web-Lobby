package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"

	"github.com/nokka/d2s"
)

var servers = map[string]string{"MyServer": "127.0.0.1:6110/", "": "127.0.0.1:6110/"}

func showChar(w http.ResponseWriter, r *http.Request) {
	path := r.URL.Path[1:]
	parts := strings.Split(path, "/")
	server := parts[0]
	characterName := parts[1]
	pathToServer := "http://" + servers[server] + "getCharacter/" + characterName
	//pathToServer := "http://127.0.0.1:6110/getCharacter/artificial"
	fmt.Println(pathToServer)
	resp, err := http.Get(pathToServer)
	fmt.Println(resp.Body)
	defer resp.Body.Close()
	file, err := ioutil.ReadAll(resp.Body)
	//fmt.Println(string(file))
	if err != nil {
		fmt.Fprintf(w, "Error:", err)
		return
	}
	/*
		file, err := ioutil.ReadAll(resp.Body)
		fmt.Fprintf(w, "Resp:", string(file), "END\n")
		if err != nil {
			fmt.Fprintf(w, "Error:", err)
			return
		}
	*/

	fmt.Println(4)
	char, err := d2s.Parse(resp.Body)
	fmt.Println(5)
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
