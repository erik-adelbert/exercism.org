package ocr

import (
	"regexp"
	"strings"
)

type digit int16

func recognizeDigit(s []byte) string {
	convert := []string{
		72:   "1",
		456:  "4",
		1240: "3",
		1096: "7",
		1264: "2",
		1400: "0",
		1432: "5",
		1464: "6",
		1496: "9",
		1528: "8",
	}

	var d digit
	for i := range s {
		if s[i] == '\n' {
			continue
		}

		d = d << 1
		if s[i] != ' ' {
			d |= 1
		}
	}

	if convert[d] != "" {
		return convert[d]
	}
	return "?"
}

func Recognize(s string) []string {

	blank := regexp.MustCompile(`(?m)^(\s+)\n`)
	delim := blank.ReplaceAll([]byte(s), []byte("$1\n%\n"))
	numbers := strings.Split(string(delim), "%")

	ocred := make([]string, 0, len(numbers))
	splitone := false
	for j, s := range numbers {
		switch {
		case len(s) == 5:
			splitone = true
			fallthrough
		case len(s) == 0:
			continue
		case splitone:
			splitone = false
			if s = numbers[j-1] + s[1:]; len(s) > 16 {
				s = s[:len(s)-1]
			}
		}

		raster := make([]string, 0)
		rlen := (len(s) / 4) - 1  // 4 lines minus one '\n'
		blen := (len(s) - 4) / 12 // 12B reblocking
		blocks := make([][]byte, blen)

		for i := range blocks {
			blocks[i] = make([]byte, 12)
		}

		nread := 0
		for _, c := range []byte(s) {
			switch {
			case c == '\n':
				continue
			default:
				bi := (nread / 3) % blen
				y := nread / rlen
				x := nread % 3

				blocks[bi][y*3+x] = c // reblock
				nread++
			}
		}

		for i := range blocks {
			raster = append(raster, recognizeDigit(blocks[i]))
		}

		if number := strings.Join(raster, ""); len(number) > 0 {
			ocred = append(ocred, number)
		}

	}
	return ocred
}
