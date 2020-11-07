package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"

	_ "github.com/lib/pq"
)

func getUser(username string) (User, error) {
	if fileMode == "DataBase" {
		return getUserFromDataBase(username)
	} else {
		return getUserFromFile(username)
	}
}

func registerUser(username string, passhash string, email string) (User, error) {
	user, err := getUser(username)
	if err == nil {
		return user, errors.New("Username is taken")
	}
	if fileMode == "Plain" {
		return registerUserInFile(username, passhash, email)
	} else {
		return registerUserInDataBase(username, passhash, email)
	}
}

func getCharacterView(w http.ResponseWriter, r *http.Request) {
	path := r.URL.Path[len("/getCharacter/"):]
	char, err := getCharacterFromFile(path)
	if err != nil {
		fmt.Fprintf(w, "Error while opening character file ", err)
		return
	}
	ans, err := json.Marshal(char)
	fmt.Fprintln(w, string(ans))
	if err != nil {
		fmt.Fprintf(w, "Error while parsign character class  ", err)
		return
	}
}

func getLadderView(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, parseLadder())
}

func getUserView(w http.ResponseWriter, r *http.Request) {
	username := r.URL.Path[len("/getUser/"):]
	user, err := getUser(username)
	if err != nil {
		fmt.Fprintf(w, "Error finding user ", err)
		return
	}
	ans, err := json.Marshal(user)
	fmt.Fprintln(w, string(ans))
	if err != nil {
		fmt.Fprintf(w, "Error while parsing ", err)
		return
	}
}

func getCharactersFromUserView(w http.ResponseWriter, r *http.Request) {
	username := r.URL.Path[len("/getCharactersFromUser/"):]
	directory := "D:/PvPGN/Magic_Builder/release/var/charinfo/" + username + "/"
	files, err := ioutil.ReadDir(directory)
	if err != nil {
		fmt.Fprintln(w, "Error: user doesn't exists! ", err)
	}
	for _, f := range files {
		if !f.IsDir() {
			fmt.Fprintln(w, f.Name())
		}
	}
}

func checkLogin(username string, passhash string) bool {
	user, _ := getUser(username)
	return passhash == user.Passhash1
}

func checkLoginView(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		if err := r.ParseForm(); err != nil {
			fmt.Fprintf(w, "Error in ParseForm() ", err)
			return
		}
		fmt.Fprintf(w, "Post from website! r.PostFrom = %v\n", r.PostForm)
		username := r.FormValue("username")
		passhash := r.FormValue("passhash")
		if checkLogin(username, passhash) {
			fmt.Fprintln(w, "OK")
		} else {
			fmt.Fprintln(w, "Error login rejected")
		}
	} else {
		fmt.Fprintln(w, "Error must be POST request but this is", r.Method)
	}
}

func registerView(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		if err := r.ParseForm(); err != nil {
			fmt.Fprintf(w, "Error in ParseForm() ", err)
			return
		}
		username := r.FormValue("username")
		passhash := r.FormValue("passhash")
		email := r.FormValue("email")
		user, err := registerUser(username, passhash, email)
		if err == nil {
			ans, err := json.Marshal(user)
			if err != nil {
				fmt.Fprintf(w, "Error while parsing ", err)
				return
			}
			fmt.Fprintln(w, string(ans))
		} else {
			if err.Error() == "Username is taken" {
				fmt.Fprintln(w, err)
			} else {
				fmt.Fprintln(w, "Error ", err)
			}
		}
	} else {
		fmt.Fprintln(w, "Error must be POST request but this is", r.Method)
	}
}

func createCharacterView(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		if err := r.ParseForm(); err != nil {
			fmt.Fprintf(w, "Error in ParseForm() ", err)
			return
		}
		username := r.FormValue("username")
		passhash := r.FormValue("passhash")
		if !checkLogin(username, passhash) {
			fmt.Fprintln(w, "Error login rejected")
			return
		}

		charname := r.FormValue("charname")
		characterClass := r.FormValue("characterClass")
		char, err := createCharacterInFile(strings.ToLower(username), strings.ToLower(charname), characterClass)
		if err == nil {
			ans, err := json.Marshal(char)
			if err != nil {
				fmt.Fprintf(w, "Error while parsing ", err)
				return
			}
			fmt.Fprintln(w, string(ans))
		} else {
			if err.Error() == "Character name is taken" {
				fmt.Fprintln(w, err)
			} else {
				fmt.Fprintln(w, "Error ", err)
			}
		}
	} else {
		fmt.Fprintln(w, "Error must be POST request but this is", r.Method)
	}
}

func getStatusView(w http.ResponseWriter, r *http.Request) {
	ans, err := getStatus()
	if err != nil {
		fmt.Fprintln(w, "Error while parsing status json", err)
	}
	fmt.Fprintln(w, string(ans))
}

func getGamelistView(w http.ResponseWriter, r *http.Request) {
	ans, err := getGamelist()
	if err != nil {
		fmt.Fprintln(w, "Error while parsing status json", err)
	}
	for game := range ans {
		fmt.Fprintln(w, string(game))
	}
}

func favicon(w http.ResponseWriter, r *http.Request) {

}

func main() {
	fmt.Println("Starting app...")
	if fileMode != "Plain" {
		fmt.Println("Connecting to database...")
		err := connectToDatabase()
		if err != nil {
			panic(err)
		}
		fmt.Println("Connected to database!")
	}
	fmt.Println("Starting API...")
	http.HandleFunc("/favicon.ico", favicon) //IDK why but python ask for this in every request
	http.HandleFunc("/getCharacter/", getCharacterView)
	http.HandleFunc("/getLadder/", getLadderView)
	http.HandleFunc("/getStatus/", getStatusView)
	http.HandleFunc("/getGamelist/", getGamelistView)
	http.HandleFunc("/getUser/", getUserView)
	http.HandleFunc("/getCharactersFromUser/", getCharactersFromUserView)
	http.HandleFunc("/checkLogin", checkLoginView)
	http.HandleFunc("/register", registerView)
	http.HandleFunc("/createCharacter", createCharacterView)
	fmt.Println("Started")
	err := http.ListenAndServe(":6110", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
