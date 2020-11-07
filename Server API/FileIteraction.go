package main

import (
	"bufio"
	"encoding/binary"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
	"strings"

	"github.com/nokka/d2s"
)

var characterClassCodes = map[string]int{
	"Amazon":      0x00,
	"Sorceress":   0x01,
	"Necromancer": 0x02,
	"Paladin":     0x03,
	"Barbarian":   0x04,
	"Druid":       0x05,
	"Assassin":    0x06,
}

func getUserFromFile(username string) (User, error) {
	directory := "D:/PvPGN/PvPGN/var/users/" + username
	file, err := os.Open(directory)
	if err != nil {
		return User{}, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	answer := map[string]string{}
	fieldRegexp := regexp.MustCompile(`^.[^"]*`)
	for scanner.Scan() {
		line := scanner.Text()
		line = line[len("\"BNET\\\\acct\\\\"):] //Line format is "BNET\\acct\\username"="user"
		field := fieldRegexp.Find([]byte(line))
		answer[string(field)] = line[len(field)+3 : len(line)-1]
	}

	lastlogin_time_int, _ := strconv.Atoi(answer["lastlogin_time"])
	userid_int, _ := strconv.Atoi(answer["userid"])
	user := User{answer["passhash1"], answer["email"], answer["username"], answer["lastlogin_ip"], answer["lastlogin_clienttag"],
		answer["lastlogin_owner"], lastlogin_time_int, userid_int, answer["ctime"]}
	return user, err
}

func registerUserInFile(username string, passhash string, email string) (User, error) {
	directory := "D:/PvPGN/PvPGN/var/users/"
	files, err := ioutil.ReadDir(directory)
	if err != nil {
		return User{}, err
	}
	newid := len(files) + 1
	data := `"BNET\\acct\\passhash1"="` + passhash + `"
"BNET\\acct\\email"="` + email + `"
"BNET\\acct\\username"="` + strings.ToLower(username) + `"
"BNET\\acct\\lastlogin_ip"="0"
"BNET\\acct\\lastlogin_clienttag"="D2XP"
"BNET\\acct\\lastlogin_owner"="Panky"
"BNET\\acct\\lastlogin_time"="0"
"BNET\\acct\\userid"="` + strconv.Itoa(newid) + `"
"BNET\\acct\\ctime"="0"`
	ioutil.WriteFile(directory+username, []byte(data), 0644)
	user, err := getUserFromFile(username)
	return user, err
}

func getCharacterFromFile(charname string) (*d2s.Character, error) {
	directory := "D:/PvPGN/Magic_Builder/release/var/charsave/"
	file, err := os.Open(directory + charname)
	defer file.Close()
	char, err := d2s.Parse(file)
	return char, err
}

func createCharInfo(username string, charname string, characterClass string) error {
	//Final folder for charinfo file
	folder := "D:/PvPGN/Magic_Builder/release/var/charinfo/" + username

	// q - byte array from clear charinfo
	s := "charinfo_" + characterClass
	file, err := os.Open("./clear_char_files/" + s)
	if err != nil {
		fmt.Println("Error opening file", "/clear_char_files/"+s)
		return err
	}

	var w []byte

	//Copying some bytes from q to w
	bs := make([]byte, 48)
	_, err = file.Read(bs)
	for i := 0; i < 48; i++ {
		w = append(w, bs[i])
	}

	//Copy character name to w
	temp := []byte(charname)
	bs = make([]byte, 16)
	_, err = file.Read(bs)
	for i := 0; i < 16; i++ {
		if i >= len(temp) {
			w = append(w, 0)
		} else {
			w = append(w, temp[i])
		}
	}
	//Copy player name to bytearray w
	temp = []byte(username)
	bs = make([]byte, 16)
	_, err = file.Read(bs)
	for i := 0; i < 16; i++ {
		if i >= len(temp) {
			w = append(w, 0)
		} else {
			w = append(w, temp[i])
		}
	}
	//Copying some bytes from q to w
	bs = make([]byte, 1)
	for {
		_, err := file.Read(bs)
		if err != nil {
			if err == io.EOF {
				break
			}
			return err
		}
		w = append(w, bs[0])
	}
	//Add info about character class
	w[188] = byte(characterClassCodes[characterClass])
	os.Mkdir(folder, 0644)
	ioutil.WriteFile(folder+"/"+charname, w, 0644)
	return nil
}

func temp_checksum(data []byte, start_value int32) int32 {
	acc := start_value
	for _, value := range data {
		temp := 0
		if acc < 0 {
			temp = 1
		}
		acc = int32((acc<<1)+int32(value)) + int32(temp)
	}
	return int32(acc)
}

func d2charsave_checksum(filename string) int32 {
	offset := 12

	var data []byte
	file, err := os.Open(filename)
	if err != nil {
		return -1
	}
	bs := make([]byte, 1)
	for {
		_, err := file.Read(bs)
		if err != nil {
			if err == io.EOF {
				break
			}
			fmt.Println("D2CHECKSUM FILE FAIL")
			return -1
		}
		data = append(data, bs[0])
	}
	checksum_byte_length := 4

	pre_data := data[:offset]
	post_data := data[offset+checksum_byte_length:]

	pre_checksum := temp_checksum(pre_data, 0)
	on_checksum := temp_checksum([]byte{0, 0, 0, 0}, pre_checksum)
	post_checksum := temp_checksum(post_data, on_checksum)

	return post_checksum
}

func createCharSave(username string, charname string, characterClass string) error {
	s := "charsave_" + characterClass
	file, err := os.Open("./clear_char_files/" + s)
	if err != nil {
		fmt.Println("Error opening file", "/clear_char_files/"+s)
		return err
	}

	//w - byte array for new charsave
	var w []byte

	//Copying some bytes from q to w
	bs := make([]byte, 12)
	_, err = file.Read(bs)
	for i := 0; i < 12; i++ {
		w = append(w, bs[i])
	}

	//Some bytes with checksum. Must be 0 to calculate checksum
	bs = make([]byte, 4)
	_, err = file.Read(bs)
	for i := 12; i < 16; i++ {
		w = append(w, 0)
	}

	//Copying some bytes from q to w
	bs = make([]byte, 4)
	_, err = file.Read(bs)
	for i := 0; i < 4; i++ {
		w = append(w, bs[i])
	}

	//Copy name to bytearray w
	temp := []byte(charname)
	bs = make([]byte, 16)
	_, err = file.Read(bs)

	for i := 0; i < 16; i++ {
		if i >= len(temp) {
			w = append(w, 0)
		} else {
			w = append(w, temp[i])
		}
	}

	//Copying some bytes from q to w
	bs = make([]byte, 4)
	_, err = file.Read(bs)
	for i := 0; i < 4; i++ {
		w = append(w, bs[i])
	}

	//Add info about character class

	//Copying some bytes from q to w
	bs = make([]byte, 1)
	for {
		_, err := file.Read(bs)
		if err != nil {
			if err == io.EOF {
				break
			}

			return err
		}
		w = append(w, bs[0])
	}
	folder := "D:/PvPGN/Magic_Builder/release/var/charsave/" + charname
	ioutil.WriteFile(folder, w, 0644)

	check := d2charsave_checksum(folder)
	temp = make([]byte, 4)
	binary.LittleEndian.PutUint32(temp, uint32(check))
	for i := 12; i < 16; i++ {
		w[i] = temp[i-12]
	}
	err = ioutil.WriteFile(folder, w, 0644)
	return err
}

func createCharacterInFile(username string, charname string, characterClass string) (*d2s.Character, error) {
	if char, err := getCharacterFromFile(charname); err == nil {
		return char, errors.New("Character name is taken")
	}
	err := createCharInfo(username, charname, characterClass)
	if err != nil {
		return nil, err
	}
	err = createCharSave(username, charname, characterClass)
	if err != nil {
		return nil, err
	}
	return getCharacterFromFile(charname)
}
