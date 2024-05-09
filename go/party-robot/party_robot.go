package partyrobot

import (
	"fmt"
	"strings"
)

// Welcome greets a person by name.
func Welcome(name string) string {
	msg := "Welcome to my party, %s!"

	return fmt.Sprintf(msg, name)
}

// HappyBirthday wishes happy birthday to the birthday person and exclaims their age.
func HappyBirthday(name string, age int) string {
	msg := "Happy birthday %s! You are now %d years old!"

	return fmt.Sprintf(msg, name, age)
}

// AssignTable assigns a table to each guest.
func AssignTable(name string, table int, neighbor, direction string, distance float64) string {
	msg := []string{
		"Welcome to my party, %s!",
		"You have been assigned to table %03d. Your table is %s, exactly %.1f meters from here.",
		"You will be sitting next to %s.",
	}

	return fmt.Sprintf(
		strings.Join(msg, "\n"), name, table, direction, distance, neighbor,
	)
}
