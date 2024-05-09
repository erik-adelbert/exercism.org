package thefarm

import (
	"errors"
	"fmt"
)

func DivideFood(fc FodderCalculator, ncow int) (float64, error) {
	var amount, factor float64
	var err error

	if amount, err = fc.FodderAmount(ncow); err != nil {
		return amount, err
	}

	if factor, err = fc.FatteningFactor(); err != nil {
		return factor, err
	}

	return factor * amount / float64(ncow), nil
}

func ValidateInputAndDivideFood(fc FodderCalculator, ncow int) (float64, error) {
	if ncow <= 0 {
		return 0, errors.New("invalid number of cows")
	}
	return DivideFood(fc, ncow)
}

type InvalidCowsError struct {
	ncow int
	msg  string
}

func (ice *InvalidCowsError) Error() string {
	return fmt.Sprintf("%d cows are invalid: %s", ice.ncow, ice.msg)
}

func ValidateNumberOfCows(ncow int) error {
	switch {
	case ncow < 0:
		return &InvalidCowsError{
			ncow: ncow,
			msg:  "there are no negative cows",
		}
	case ncow == 0:
		return &InvalidCowsError{
			ncow: ncow,
			msg:  "no cows don't need food",
		}
	}
	return nil
}
