package say

import (
	"fmt"
	"strings"
)

func Say(n int64) (string, bool) {
	var out []string

	switch {
	case n < 0, n >= 1_000_000_000_000:
		return "", false
	case n == 0:
		return numbers[0], true
	}

	var powers = struct {
		v []int64
		s []string
	}{
		v: []int64{1_000_000_000, 1_000_000, 1_000},
		s: []string{"billion", "million", "thousand"},
	}

	for i, d := range powers.v {
		if n := n / d; n > 0 {
			out = append(out, fmt.Sprintf("%s %s", say999(n), powers.s[i]))
		}
		n %= d
	}

	if n > 0 {
		out = append(out, say999(n))
	}

	return strings.Join(out, " "), true
}

func say999(n int64) string {
	hund, low := n/100, n%100

	switch {
	case hund > 0 && low > 0:
		return fmt.Sprintf("%s hundred %s", numbers[hund], say99(low))
	case hund > 0:
		return fmt.Sprintf("%s hundred", numbers[hund])
	}

	return say99(low)
}

func say99(n int64) string {
	ten, low := 10*(n/10), n%10

	if ten >= 20 && low != 0 {
		return fmt.Sprintf("%s-%s", numbers[ten], numbers[low])
	}
	return numbers[n]
}

var numbers = []string{
	"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
	"ten", "eleven", "twelwe", "thirteen", "fourteen", "fifeen", "sixteen", "seventeen", "eighteen", "nineteen",
	20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety",
}
