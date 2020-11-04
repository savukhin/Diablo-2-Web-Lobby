package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"

	"github.com/nokka/d2s"
	"github.com/reiver/go-telnet"
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
func getStatus(w http.ResponseWriter, r *http.Request) {
	conn, _ := telnet.DialTo("127.0.0.1:8888")
	conn.Write([]byte("abcd123\n"))
	telnetReadUntil(">", conn)
	conn.Write([]byte("status\n"))
	answer := strings.Split(telnetReadUntil(">", conn), "\n")
	maxGames, _ := strconv.Atoi(strings.Split(answer[2][:len(answer[2])-1], " ")[3])
	currentGames, _ := strconv.Atoi(strings.Split(answer[3][:len(answer[3])-1], " ")[3])
	//maxUsers, _ := strconv.Atoi(strings.Split(answer[4][:len(answer[4])-1], " ")[3])
	currentUsers, _ := strconv.Atoi(strings.Split(answer[4][:len(answer[4])-1], " ")[4])
	res := map[string]int{
		"maximumCountOfGames": maxGames,
		"runningCountOfGames": currentGames,
		//"maximumCountOfUsers": maxUsers,
		"runningCountOfUsers": currentUsers,
	}

	jsonString, _ := json.Marshal(res)
	fmt.Fprintln(w, string(jsonString))
}

func getGames() [][]byte {
	conn, _ := telnet.DialTo("127.0.0.1:8888")
	conn.Write([]byte("abcd123\n"))
	telnetReadUntil(">", conn)
	conn.Write([]byte("gl\n"))
	answer := telnetReadUntil(">", conn)

	validRegexp := regexp.MustCompile(`\|[^\|]*\|`)
	games := validRegexp.FindAll([]byte(answer), -1)
	return games
}

func getGamelist(w http.ResponseWriter, r *http.Request) {
	games := getGames()
	for i := range games {
		var raw []string
		for _, val := range strings.Split(string(games[i])[1:len(games[i])-1], " ") {
			if val != "" {
				raw = append(raw, val)
			}
		}

		game := map[string]string{"No": raw[0],
			"GameName": raw[1]}
		if len(raw) == 10 { //Game doesn't have a Password
			game["ID"] = raw[2]
			game["GameVer"] = raw[3]
			game["Type"] = raw[4]
			game["Difficulty"] = raw[5]
			game["Ladder"] = raw[6]
			game["Users"] = raw[7]
			game["CreateTime"] = raw[8]
			game["Disable"] = raw[9]
		} else {
			game["password"] = raw[2]
			game["ID"] = raw[3]
			game["GameVer"] = raw[4]
			game["Type"] = raw[5]
			game["Difficulty"] = raw[6]
			game["Ladder"] = raw[7]
			game["Users"] = raw[8]
			game["CreateTime"] = raw[9]
			game["Disable"] = raw[10]
		}
		jsonString, _ := json.Marshal(game)
		fmt.Fprintf(w, string(jsonString))
	}
}

func favicon(w http.ResponseWriter, r *http.Request) {

}

func telnetReadUntil(symbol string, conn *telnet.Conn) string {
	bs := make([]byte, 1)
	s := ""
	for string(bs) != ">" {
		conn.Read(bs)
		s += string(bs)
	}
	return s
}

func main() {
	fmt.Println("Starting app...")
	http.HandleFunc("/favicon.ico", favicon)
	http.HandleFunc("/getCharacter/", getCharacter)
	http.HandleFunc("/getLadder/", getLadder)
	http.HandleFunc("/getStatus/", getStatus)
	http.HandleFunc("/getGamelist/", getGamelist)
	fmt.Println("Started")
	err := http.ListenAndServe(":6110", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
