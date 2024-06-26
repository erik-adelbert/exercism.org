package booking

import (
	"fmt"
	"time"
)

// Schedule returns a time.Time from a string containing a date.
func Schedule(date string) time.Time {
	t, _ := time.Parse("1/02/2006 15:04:05", date)
	return t
}

// HasPassed returns whether a date has passed.
func HasPassed(date string) bool {
	t, _ := time.Parse("January 2, 2006 15:04:05", date)
	return time.Now().After(t)
}

// IsAfternoonAppointment returns whether a time is in the afternoon.
func IsAfternoonAppointment(date string) bool {
	t, _ := time.Parse("Monday, January 2, 2006 15:04:05", date)
	fmt.Println(t, t.Hour())
	return 12 <= t.Hour() && t.Hour() <= 18
}

// Description returns a formatted string of the appointment time.
func Description(date string) string {
	t, _ := time.Parse("1/2/2006 15:04:05", date)
	when := t.Format("Monday, January 2, 2006, at 15:04")

	return fmt.Sprintf("You have an appointment on %s.", when)
}

// AnniversaryDate returns a Time with this year's anniversary.
func AnniversaryDate() time.Time {
	date := fmt.Sprintf("09/15/%d", time.Now().Year())
	anniversary, _ := time.Parse("01/02/2006", date)
	return anniversary
}
