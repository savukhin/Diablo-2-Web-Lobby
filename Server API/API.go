package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/nokka/d2s"
)

const directory = "D:/PvPGN/Magic_Builder/release/var/charsave/"

func getCharacter(w http.ResponseWriter, r *http.Request) {
	path := r.URL.Path[len("/getCharacter/"):]
	file, err := os.Open(directory + path)
	defer file.Close()
	char, _ := d2s.Parse(file)
	ans, err := json.Marshal(char)
	fmt.Println(char)
	fmt.Fprintln(w, string(ans))
	if err != nil {
		fmt.Fprintf(w, "Error while opening .d2s file ", err)
		return
	}
}

func getLadder(w http.ResponseWriter, r *http.Request) {

	fmt.Fprintf(w, parseLadder())
}

//TODO
func getUser(w http.ResponseWriter, r *http.Request) {

}

//TODO
func getGamelist(w http.ResponseWriter, r *http.Request) {

}

func favicon(w http.ResponseWriter, r *http.Request) {

}

type Foo struct {
	Number     string
	Title      string
	Charname   string
	prefix     string
	experience string
	class      string
	sex        string
	level      string
	difficulty string
	hc         string
	died       string
}

func main() {

	fmt.Println("Starting app...")
	http.HandleFunc("/favicon.ico", favicon)
	http.HandleFunc("/getCharacter/", getCharacter)
	http.HandleFunc("/getLadder/", getLadder)
	http.HandleFunc("/getUser/", getUser)
	http.HandleFunc("/getGamelist/", getGamelist)
	fmt.Println("Started")
	err := http.ListenAndServe(":6110", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}

	datas := make(map[int][]Foo)

	for i := 0; i < 10; i++ {
		datas[i] = append(datas[i], Foo{"dd", "test", "test", "test", "test", "test", "test", "test", "test", "test", "test"})
	}

	jsonString, _ := json.Marshal(datas)

	fmt.Println(datas)
	fmt.Println("-------------------------------")
	fmt.Println(string(jsonString))

}
