package main

import (
	"bufio"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"time"

	_ "github.com/lib/pq"
	"github.com/nokka/d2s"
)

func getAllCharacters() ([]byte, error) {
	directory := pathToCharSaveFolder
	files, err := ioutil.ReadDir(directory)
	if err != nil {
		fmt.Println("Error while opening character dir")
		return nil, err
	}
	var characters []*d2s.Character
	for _, f := range files {
		if !f.IsDir() {
			char, err := getCharacterFromFile(f.Name())
			if err != nil {
				//fmt.Println("Error while parsing ", f.Name())
			} else {
				characters = append(characters, char)
			}
		}
	}
	answer, err := json.Marshal(characters)
	return answer, nil
}

func getAllGames() ([]byte, error) {
	gamelist, err := getGamelist()
	if err != nil {
		return nil, err
	}
	var gameInfos []GameInfo
	for _, game := range *gamelist {
		id, err := strconv.Atoi(game["ID"])
		if err != nil {
			continue
		}
		info, err := getGameInfoById(id)
		if err != nil {
			continue
		}
		gameInfos = append(gameInfos, *info)
	}
	jsonGameInfos, err := json.Marshal(gameInfos)
	if err != nil {
		return nil, err
	}

	return jsonGameInfos, nil
}

func getAllUsers() ([]byte, error) {
	if fileMode == "Plain" {
		return getAllUsersFromFile()
	} else {
		return getAllUsersFromDataBase()
	}
}

func readConfig() error {
	file, err := os.Open("config.conf")
	if err != nil {
		return err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	config := map[string]string{}
	for scanner.Scan() {
		line := scanner.Text()
		if len(line) == 0 || line[0] == '#' { // Comment
			continue
		}

		data := strings.Split(line, " = ")
		if len(data) != 2 {
			return errors.New("Error in config file")
		}

		value := data[1]
		config[data[0]] = value[1 : len(value)-1]
	}

	server = config["server"]
	serviceAddr = config["serviceAddr"]
	fileMode = config["fileMode"]
	pathToUsersFolder = config["pathToUsersFolder"]
	prefix = config["prefix"]
	host = config["host"]
	port, err = strconv.Atoi(config["port"])
	if err != nil {
		return err
	}
	DataBaseUser = config["DataBaseUser"]
	DataBasePassword = config["DataBasePassword"]
	dbname = config["DataBaseName"]
	pathToCharSaveFolder = config["pathToCharSaveFolder"]
	pathToLadderFile = config["pathToLadderFile"]
	D2GSPassword = config["D2GSPassword"]
	D2GSAddress = config["D2GSAddress"]

	if err := scanner.Err(); err != nil {
		return err
	}

	return nil
}

func main() {
	fmt.Println("Starting app...")
	fmt.Println("Reading config...")
	err := readConfig()
	if err != nil {
		panic(err)
	}
	fmt.Println("Success")
	if fileMode != "Plain" {
		fmt.Println("Connecting to database...")
		err = connectToDatabase()
		if err != nil {
			panic(err)
		}
		fmt.Println("Connected to database!")
	}
	fmt.Println("Try to get access to characters")
	characters, err := getAllCharacters()
	if err != nil {
		fmt.Println("Error")
		return
	}
	fmt.Println("Success!")

	fmt.Println("Try to get access to ladder")
	ladder, err := parseLadder()
	if err != nil {
		fmt.Println("Error")
		return
	}
	fmt.Println("Success")

	fmt.Println("Try to get access to status")
	status, err := getStatus()
	if err != nil {
		fmt.Println("Error")
		return
	}
	fmt.Println("Success")

	fmt.Println("Try to get access to gamelist")
	_, err = getAllGames()
	if err != nil {
		fmt.Println("Error")
		return
	}
	fmt.Println("Success")

	fmt.Println("Try to get access to users")
	users, err := getAllCharacters()
	if err != nil {
		fmt.Println("Error")
		return
	}
	fmt.Println("Success")

	fmt.Println("Started")
	lostConnection := false

	for {
		//query := map[string]string{"server": server}
		query := url.Values{}
		query.Add("server", server)

		new_characters, err := getAllCharacters()
		if err != nil {
			query.Add("characters", string(characters))
		} else {
			query.Add("characters", string(new_characters))
			characters = new_characters
		}

		new_ladder, err := parseLadder()
		if err != nil {
			query.Add("ladder", ladder)
		} else {
			query.Add("ladder", new_ladder)
			ladder = new_ladder
		}

		gamelist, err := getAllGames()
		if err != nil {
			query.Add("gamelist", "")
		} else {
			query.Add("gamelist", string(gamelist))
		}

		new_users, err := getAllUsers()
		if err != nil {
			query.Add("users", string(users))
		} else {
			query.Add("users", string(new_users))
			users = new_users
		}

		new_status, err := getStatus()
		if err != nil {
			query.Add("status", string(status))
		} else {
			query.Add("status", string(new_status))
			status = new_status
		}

		_, err = http.PostForm(serviceAddr, query)
		if err != nil {
			fmt.Println("Troubles with connection to server. Trying to reconnect...")
			lostConnection = true
		} else if err == nil && lostConnection {
			fmt.Println("Connection restored")
			lostConnection = false
		}

		time.Sleep(time.Second)
	}

}
