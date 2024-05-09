package collatzconjecture

import "errors"

type cache []int

const CacheSize = 1_000_000

var cycles cache

func init() {
	cycles = make(cache, CacheSize)
	CollatzConjecture(CacheSize)
}

func CollatzConjecture(n int) (int, error) {
	if n <= 0 {
		return 0, errors.New("invalid negative or zero integer argument")
	}

	switch {
	case n == 1:
		return 0, nil
	case n <= CacheSize && cycles[n-1] > 0:
		return cycles[n-1], nil
	default:
		var nsub int

		nstep := 1
		if n&1 == 0 {
			nsub, _ = CollatzConjecture(n / 2)
		} else {
			nsub, _ = CollatzConjecture(3*n + 1)
		}
		nstep += nsub

		if n <= CacheSize {
			cycles[n-1] = nstep
		}
		return nstep, nil
	}
}
