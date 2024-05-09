package palindrome

import "fmt"

type Product struct {
	Product        int      // palindromic, of course
	Factorizations [][2]int // list of all possible two-factor factorizations of Product, within given limits, in order
}

func (a Product) cmp(b Product) int {
	return a.Product - b.Product
}

func (a *Product) addFactors(b Product) {
	a.Factorizations = append(a.Factorizations, b.Factorizations...)
}

func Products(fmin, fmax int) (pmin, pmax Product, err error) {
	// init min/max value to +INF/-INF
	M := max(abs(fmin), abs(fmax))
	pmin.Product = (M * M) + 1
	pmax.Product = -pmin.Product

	// validate args
	if fmin > fmax {
		err = errorf("fmin > fmax")
		return
	}

	for i := fmin; i <= fmax; i++ {
		for j := i; j <= fmax; j++ {
			if isPalindromic(i * j) {
				p := Product{i * j, [][2]int{{i, j}}}

				// check min
				switch {
				case pmin.cmp(p) > 0:
					pmin = p
				case pmin.cmp(p) == 0:
					pmin.addFactors(p)
				}

				// check max
				switch {
				case pmax.cmp(p) < 0:
					pmax = p
				case pmax.cmp(p) == 0:
					pmax.addFactors(p)
				}
			}
		}
	}

	if len(pmin.Factorizations) == 0 {
		err = errorf("no palindromes")
	}

	return
}

func isPalindromic(n int) bool {
	if n < 0 || n%10 == 0 && n != 0 {
		return false
	}

	rev := 0
	for n > rev {
		rev = rev*10 + n%10
		n /= 10
	}
	return n == rev || n == rev/10 // tricky! it removes the middle digit
}

func errorf(s string) error {
	return fmt.Errorf("%s...", s)
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
