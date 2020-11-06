package main

import (
	"database/sql"
	"encoding/json"
	"strings"

	"fmt"
	"reflect"

	_ "github.com/lib/pq"
)

const (
	prefix           = "pvpgn_"
	host             = "localhost"
	port             = 5433
	DataBaseUser     = "postgres"
	DataBasePassword = "1qw34r78"
	dbname           = "PvPGN"
)

type pvpgn_bnet struct {
	Uid                      int
	Acct_username            NullString
	Username                 string
	Acct_userid              NullInt64
	Acct_passhash1           string
	Acct_email               NullString
	Auth_admin               NullString
	Auth_normallogin         NullString
	Auth_changepass          NullString
	Auth_changeprofile       NullString
	Auth_botlogin            NullString
	Auth_operator            NullString
	New_at_team_flag         NullInt64
	Auth_lock                NullString
	Auth_locktime            NullInt64
	Auth_lockreason          NullString
	Auth_mute                NullString
	Auth_mutetime            NullInt64
	Auth_mutereason          NullString
	Auth_command_groups      NullString
	Acct_lastlogin_time      NullInt64
	Acct_lastlogin_owner     NullString
	Acct_lastlogin_clienttag NullString
	Acct_lastlogin_ip        NullString
	Acct_ctime               NullString
}

type User struct {
	Passhash1           string `json:"passhash"`
	Email               string `json:"email"`
	Username            string `json:"username"`
	Lastlogin_ip        string `json:"lastlogin_ip"`
	Lastlogin_clienttag string `json:"lastlogin_clienttag"`
	Lastlogin_owner     string `json:"lastlogin_owner"`
	Lastlogin_time      int    `json:"lastlogin_time"`
	Userid              int    `json:"userid"`
	Ctime               string `json:"ctime"`
}

var db *sql.DB

func connectToDatabase() error {
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+
		"password=%s dbname=%s sslmode=disable",
		host, port, DataBaseUser, DataBasePassword, dbname)
	db, _ = sql.Open("postgres", psqlInfo)
	//defer db.Close()

	err := db.Ping()
	if err != nil {
		panic(err)
	}
	return err
}

type NullString sql.NullString

// Scan implements the Scanner interface for NullInt64
func (ns *NullString) Scan(value interface{}) error {
	var s sql.NullString
	if err := s.Scan(value); err != nil {
		return err
	}

	// if nil then make Valid false
	if reflect.TypeOf(value) == nil {
		*ns = NullString{s.String, false}
	} else {
		*ns = NullString{s.String, true}
	}

	return nil
}

func (ns *NullString) MarshalJSON() ([]byte, error) {
	if !ns.Valid {
		return []byte("null"), nil
	}
	return json.Marshal(ns.String)
}

// NullInt64 is an alias for sql.NullInt64 data type
type NullInt64 sql.NullInt64

// Scan implements the Scanner interface for NullInt64
func (ni *NullInt64) Scan(value interface{}) error {
	var i sql.NullInt64
	if err := i.Scan(value); err != nil {
		return err
	}

	// if nil then make Valid false
	if reflect.TypeOf(value) == nil {
		*ni = NullInt64{i.Int64, false}
	} else {
		*ni = NullInt64{i.Int64, true}
	}
	return nil
}

func (ni *NullInt64) MarshalJSON() ([]byte, error) {
	if !ni.Valid {
		return []byte("null"), nil
	}
	return json.Marshal(ni.Int64)
}

func getUserFromDataBase(username string) (User, error) {
	rows, err := db.Query("SELECT * FROM " + prefix + "bnet where username='" + username + "';")
	if err != nil {
		panic(err)
	}
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	user := pvpgn_bnet{}
	rows.Next()
	err = rows.Scan(&user.Uid, &user.Acct_username, &user.Username, &user.Acct_userid, &user.Acct_passhash1, &user.Acct_email, &user.Auth_admin, &user.Auth_normallogin, &user.Auth_changepass,
		&user.Auth_changeprofile, &user.Auth_botlogin, &user.Auth_operator, &user.New_at_team_flag, &user.Auth_lock, &user.Auth_locktime, &user.Auth_lockreason, &user.Auth_mute,
		&user.Auth_mutetime, &user.Auth_mutereason, &user.Auth_command_groups, &user.Acct_lastlogin_time, &user.Acct_lastlogin_owner, &user.Acct_lastlogin_clienttag, &user.Acct_lastlogin_ip, &user.Acct_ctime)

	if err != nil {
		fmt.Println(err)
		return User{}, err
	}
	defer rows.Close()

	final_user := User{user.Acct_passhash1, user.Acct_email.String, user.Username, user.Acct_lastlogin_ip.String, user.Acct_lastlogin_clienttag.String, user.Acct_lastlogin_owner.String,
		int(user.Acct_lastlogin_time.Int64), user.Uid, user.Acct_ctime.String}
	return final_user, err
}

func registerUserInDataBase(username string, passhash string, email string) (User, error) {
	rows, _ := db.Query("SELECT COUNT(*) FROM " + prefix + "bnet;")
	rows.Next()
	newid := 0
	err := rows.Scan(&newid)
	if err != nil {
		return User{}, err
	}
	sqlStatement := `
	INSERT INTO ` + prefix + `bnet (uid, acct_username, username, acct_userid, acct_passhash1, acct_email, auth_admin, auth_normallogin, auth_changepass, auth_changeprofile, auth_botlogin,	
		auth_operator, new_at_team_flag, auth_lock, auth_locktime, auth_lockreason, auth_mute, auth_mutetime, auth_mutereason, auth_command_groups, acct_lastlogin_time, acct_lastlogin_owner,
		acct_lastlogin_clienttag, acct_lastlogin_ip, acct_ctime)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25)`

	_, err = db.Exec(sqlStatement, newid,
		username,
		strings.ToLower(username),
		newid,
		passhash,
		email,
		"false",
		"true",
		"true",
		"true",
		"false",
		"false",
		0,
		"false",
		0,
		nil,
		"false",
		0,
		nil,
		"1",
		0,
		"Panky",
		"D2XP",
		"192.168.1.14",
		"0")

	user, _ := getUserFromDataBase(username)
	return user, err
}
