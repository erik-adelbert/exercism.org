// Package ledger provides functionality for formatting ledger entries into a string with a table-like structure.
package ledger

import (
	"errors"
	"fmt"
	"slices"
	"strings"
	"time"

	"golang.org/x/text/language"
	"golang.org/x/text/message"
)

// Entry represents a single ledger entry with a date, description, and change amount.
type Entry struct {
	Date        string // "YYYY-MM-DD"
	Description string // free text
	Change      int    // in cents
}

// Compare entries by date, description, and change amount
func (a Entry) Compare(b Entry) int {
	switch {
	case a.Date != b.Date:
		return strings.Compare(a.Date, b.Date)
	case a.Description != b.Description:
		return strings.Compare(a.Description, b.Description)
	}
	return a.Change - b.Change
}

// FormatLedger formats a slice of ledger entries into a string with a table-like structure.
// It sorts the entries by date, description, and change amount, and formats them according
// to the specified currency and locale.
func FormatLedger(currency string, localeTag string, input []Entry) (string, error) {
	// Get locale infos
	locale, ok := LOCALES[localeTag]

	// Validate arguments
	switch {
	case !ok:
		return localeTag, ErrUnsupportedLocale
	case currency != "USD" && currency != "EUR":
		return currency, ErrUnsupportedCurrency
	}

	// Copy input slice to avoid modifying original data
	entries := make([]Entry, len(input))
	copy(entries, input)

	// Sort entries by date, description, and change amount
	slices.SortFunc(entries, func(a, b Entry) int { return a.Compare(b) })

	// Initialize table with headers based on locale
	var table = []string{locale.head}

	// Append formatted entries to table
	table = slices.Grow(table, 2+len(entries)) // 1 header + 1 empty end row + entries
	for _, entry := range entries {
		row, err := locale.entryFormat(entry, currency)
		if err != nil {
			return "", err
		}
		table = append(table, row)
	}
	table = append(table, "") // extra empty row at the end

	// Join table rows into a single string with newline separators
	return strings.Join(table, "\n"), nil
}

type localeInfos struct {
	lang language.Tag
	head string // Ledger header
	date string // Format string for currency date
	neg  string // Format string for negative currency and amount
	pos  string // Format string for positive currency and amount
}

// Locale-specific formatting settings
var LOCALES = map[string]localeInfos{
	"en-US": {
		lang: language.AmericanEnglish,
		head: "Date       | Description               | Change",
		date: "01/02/2006", // time.Parse layout
		neg:  "(%s%0.2f)",  // "($12,345.67)"
		pos:  " %s%0.2f ",  // " €12,345.67 "
	},
	"nl-NL": {
		lang: language.Dutch,
		head: "Datum      | Omschrijving              | Verandering",
		date: "02-01-2006", // time.Parse layout
		neg:  "%s %0.2f-",  // "€ 1.234,56-"
		pos:  "%s %0.2f ",  // "$ 1.234,56 "
	},
}

// entryFormat formats a single ledger entry row by aligning the date,
// description, and change columns based on the locale.
func (li localeInfos) entryFormat(e Entry, currency string) (string, error) {
	// Format date according to locale
	date, err := li.dateFormat(e.Date)
	if err != nil {
		return date, err
	}

	// Format change amount according to currency and locale
	change := li.changeFormat(e.Change, currency)

	// Build formatted row
	return tabulate(" | ", []column{
		{width: 10, align: Left, content: date},
		{width: 25, align: Left, content: e.Description},
		{width: 13, align: Right, content: change},
	}), nil
}

// dateFormat formats the date string based on the locale.
func (li localeInfos) dateFormat(date string) (string, error) {
	parsed, err := time.Parse("2006-01-02", date)
	if err != nil {
		return date, err
	}

	// Format date based on locale and Go.Time
	return parsed.Format(li.date), nil
}

// changeFormet formats the change amount based on the currency symbol and locale.
func (li localeInfos) changeFormat(change int, currency string) string {
	// Map currency code to symbol
	switch currency {
	case "USD":
		currency = "$"
	case "EUR":
		currency = "€"
	}

	// Determine if change amount is negative and convert to absolute value
	var neg bool
	neg, change = sigabs(change)

	// Convert change amount from cents to float with 2 decimal places
	amount := float64(change) / 100

	// Select locale-specific formatting settings
	lang := message.NewPrinter(li.lang)

	// Format change amount with currency symbol sign and decimal places
	if neg {
		return lang.Sprintf(li.neg, currency, amount)
	}
	return lang.Sprintf(li.pos, currency, amount)
}

var (
	ErrUnsupportedCurrency = errors.New("unsupported currency")
	ErrUnsupportedLocale   = errors.New("unsupported locale")
)

type column struct {
	content string
	width   int
	align   int
}

const (
	Left = iota + 1
	Right
)

// Concatenate formatted columns with the given separator
func tabulate(sep string, layout []column) string {

	const minWidth = 4 // minimum column width

	// Helper function to align text within a column
	column := func(col column) string {
		n, align, s := max(col.width, minWidth), col.align, col.content

		if len(s) > n {
			s = s[:n-3] + "..."
		}

		colfmts := []string{
			Left:  fmt.Sprintf("%%-%ds", n),
			Right: fmt.Sprintf("%%%ds", n),
		}

		return fmt.Sprintf(colfmts[align], s)
	}

	row := make([]string, len(layout))
	for i := range layout {
		row[i] = column(layout[i])
	}

	return strings.Join(row, sep)
}

// sigabs takes an integer and returns a boolean indicating whether
// it's negative and its absolute value.
func sigabs(n int) (bool, int) {
	if n < 0 {
		return true, -n
	}
	return false, n
}
