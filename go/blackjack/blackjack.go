package blackjack

import "slices"

// ParseCard returns the integer value of a card following blackjack ruleset.
func ParseCard(card string) int {

	switch card {
	case "ace":
		return 11
	case "ten", "jack", "queen", "king":
		return 10
	default:
		values := []string{
			2: "two", 3: "three", 4: "four", 5: "five",
			6: "six", 7: "seven", 8: "eight", 9: "nine",
		}
		value := slices.Index(values, card)
		if value == -1 {
			return 0
		}
		return value
	}
}

// FirstTurn returns the decision for the first turn, given two cards of the
// player and one card of the dealer.
func FirstTurn(card1, card2, dealerCard string) string {
	c, d := ParseCard(card1)+ParseCard(card2), ParseCard(dealerCard)
	switch {
	case c == 22:
		return "P"
	case c == 21 && d < 10:
		return "W"
	case c >= 17, c >= 12 && d < 7:
		return "S"
	default:
		return "H"
	}
}
