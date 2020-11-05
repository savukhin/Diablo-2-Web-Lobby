package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

	_ "github.com/lib/pq"
	"github.com/nokka/d2s"
)

const directory = "D:/PvPGN/Magic_Builder/release/var/charsave/"

func getCharacter(w http.ResponseWriter, r *http.Request) {
	path := r.URL.Path[len("/getCharacter/"):]
	file, err := os.Open(directory + path)
	defer file.Close()
	char, _ := d2s.Parse(file)
	ans, err := json.Marshal(char)
	fmt.Fprintln(w, string(ans))
	if err != nil {
		fmt.Fprintf(w, "Error while opening .d2s file ", err)
		return
	}
}

func getLadder(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, parseLadder())
}

func getUserFromFile(username string) (User, error) {
	directory := "D:/PvPGN/PvPGN/var/users/" + username
	file, err := os.Open(directory)
	if err != nil {
		return User{}, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	scanner.Scan()
	passhash := scanner.Text()
	passhash = passhash[len("\"BNET\\\\acct\\\\passhash1\"=\"") : len(passhash)-1]

	scanner.Scan()
	email := scanner.Text()
	email = email[len("\"BNET\\\\acct\\\\email\"=\"") : len(email)-1]

	scanner.Scan()
	scanner.Text() //This is for username

	scanner.Scan()
	lastlogin_ip := scanner.Text()
	lastlogin_ip = lastlogin_ip[len("\"BNET\\\\acct\\\\lastlogin_ip\"=\"") : len(lastlogin_ip)-1]

	scanner.Scan()
	lastlogin_clienttag := scanner.Text()
	lastlogin_clienttag = lastlogin_clienttag[len("\"BNET\\\\acct\\\\lastlogin_clienttag\"=\"") : len(lastlogin_clienttag)-1]

	scanner.Scan()
	lastlogin_owner := scanner.Text()
	lastlogin_owner = lastlogin_owner[len("\"BNET\\\\acct\\\\lastlogin_owner\"=\"") : len(lastlogin_owner)-1]

	scanner.Scan()
	lastlogin_time := scanner.Text()
	lastlogin_time = lastlogin_time[len("\"BNET\\\\acct\\\\lastlogin_time\"=\"") : len(lastlogin_time)-1]

	scanner.Scan()
	userid := scanner.Text()
	userid = userid[len("\"BNET\\\\acct\\\\userid\"=\"") : len(userid)-1]

	scanner.Scan()
	ctime := scanner.Text()
	ctime = ctime[len("\"BNET\\\\acct\\\\ctime\"=\"") : len(ctime)-1]

	lastlogin_time_int, _ := strconv.Atoi(lastlogin_time)
	userid_int, _ := strconv.Atoi(userid)
	user := User{passhash, email, username, lastlogin_ip, lastlogin_clienttag, lastlogin_owner, lastlogin_time_int, userid_int, ctime}
	return user, err
}

func getUser(w http.ResponseWriter, r *http.Request) {
	username := r.URL.Path[len("/getUser/"):]
	user, err := getUserFromDataBase(username)
	//user, err := getUserFromFile(username)
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

func favicon(w http.ResponseWriter, r *http.Request) {

}

func main() {
	fmt.Println("Starting app...")
	getUserFromFile("savukhin")
	fmt.Println("Connecting to database...")
	err := connectToDatabase()
	if err != nil {
		panic(err)
	}

	fmt.Println("Connected to database!")
	fmt.Println("Starting API...")
	http.HandleFunc("/favicon.ico", favicon)
	http.HandleFunc("/getCharacter/", getCharacter)
	http.HandleFunc("/getLadder/", getLadder)
	http.HandleFunc("/getStatus/", getStatus)
	http.HandleFunc("/getGamelist/", getGamelist)
	http.HandleFunc("/getUser/", getUser)
	fmt.Println("Started")
	err = http.ListenAndServe(":6110", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
