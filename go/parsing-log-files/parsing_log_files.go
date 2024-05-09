package parsinglogfiles

import (
	"fmt"
	rex "regexp"
	"strings"
)

func IsValidLine(text string) bool {
	return rex.MustCompile(`^\[(TRC|DBG|INF|WRN|ERR|FTL)\]`).MatchString(text)
}

func SplitLogLine(text string) []string {
	return rex.MustCompile(`<\W*>`).Split(text, -1)
}

func CountQuotedPasswords(lines []string) int {
	re := rex.MustCompile(`".*[Pp][aA][sS][sS][wW][oO][rR][dD].*"`)
	return len(re.FindAllString(strings.Join(lines, "\n"), -1))
}

func RemoveEndOfLineText(text string) string {
	re := rex.MustCompile(`end-of-line(\d)+`)
	return re.ReplaceAllString(text, "")
}

func TagWithUserName(lines []string) []string {
	re := rex.MustCompile(`User\s+(\w+)`)

	for i := range lines {
		matches := re.FindStringSubmatch(lines[i])
		if len(matches) == 2 {
			lines[i] = fmt.Sprintf("[USR] %s %s", matches[1], lines[i])
		}
	}
	return lines
}
