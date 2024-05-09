package forth

import (
	"errors"
	"strconv"
	"strings"
)

const SIZEHINT = 8

// Forth executes Forth-like commands and returns the final stack state.
func Forth(input []string) ([]int, error) {
	SYMS = make(map[string][]fObject, SIZEHINT)
	tape := newStack(SIZEHINT)

	for i := range input {
		var prog []fObject
		var err error

		if prog, err = parse(input[i]); err != nil {
			return nil, err
		}

		if err := eval(tape, prog); err != nil {
			return nil, err
		}
	}

	return tape.trail(), nil
}

// Operation codes / types
const (
	NOP = iota
	INT
	ADD
	SUB
	MUL
	DIV
	DUP
	DRP
	SWP
	OVR
	STR
	DEF
	NIL
)

// string to opcode mapping
var code = map[string]int{
	"+":    ADD,
	"-":    SUB,
	"*":    MUL,
	"/":    DIV,
	"DUP":  DUP,
	"DROP": DRP,
	"SWAP": SWP,
	"OVER": OVR,
	":":    DEF,
	";":    NIL,
}

// fObject represents an operation or value in Forth-like program.
type fObject struct {
	key string
	op  int
	val int
}

// Symbol table
var SYMS = map[string][]fObject{}

// parse parses a line of Forth-like commands.
func parse(line string) ([]fObject, error) {
	line = strings.ToUpper(line)

	var tokens []fObject

	var define bool
	for _, word := range strings.Fields(line) {
		// parse number
		n, err := strconv.Atoi(word)
		switch {
		default:
			// unexpected error, raise!
			return nil, err
		case err == nil:
			if define {
				return nil, errIllegalOperation
			}
			tokens = append(tokens, fObject{
				op:  INT,
				val: n,
			})
			continue
		case errors.Is(err, strconv.ErrSyntax):
			// it is not a number, proceed!
		}

		// parse pending definition symbol
		if define {
			tokens = append(tokens, fObject{
				op:  DEF,
				key: word,
			})
			define = false
			continue
		}

		// check for an already defined symbol
		if sub, ok := SYMS[word]; ok {
			tokens = append(tokens, sub...)
			continue
		}

		// parse op
		if op, ok := code[word]; ok {
			switch op {
			case DEF:
				define = true // pending definition
			default:
				tokens = append(tokens, fObject{
					op:  op,
					key: word,
				})
			}
			continue
		}

		// catch all
		tokens = append(tokens, fObject{
			op:  STR,
			key: word,
		})
	}

	return tokens, nil
}

// eval evaluates Forth-like program and performs corresponding operations on the stack.
func eval(s *stack, prog []fObject) error {
	for i := 0; i < len(prog); i++ {
		obj := prog[i]

		switch obj.op {
		case INT: // number
			s.push(obj.val)

		case STR: // variable
			if sub, ok := SYMS[obj.key]; ok {
				if err := eval(s, sub); err != nil {
					return err
				}
			} else {
				return errUndefinedVariable
			}

		case DEF: // definition
			sub := make([]fObject, 0) // new subcommand
			// read ahead and fill
			for i++; prog[i].op != NIL; {
				sub = append(sub, prog[i])
				if i += 1; i >= len(prog) {
					return errSyntaxError
				}
			}
			// store
			SYMS[obj.key] = sub

		case ADD, SUB, MUL, DIV, OVR, SWP: // binary op
			if s.len() < 2 {
				return errIllegalOperation
			}

			b, a := s.pop(), s.pop()
			switch obj.op {
			case ADD:
				s.push(a + b)
			case SUB:
				s.push(a - b)
			case MUL:
				s.push(a * b)
			case DIV:
				if b == 0 {
					return errDivideByZero
				}
				s.push(a / b)

			// binary stack manipulation
			case OVR:
				s.push(a)
				fallthrough
			case SWP:
				s.push(b)
				s.push(a)
			}

		// unary stack manipulation
		case DUP, DRP:
			if s.empty() {
				return errIllegalOperation
			}

			a := s.pop() // DROP
			if obj.op == DUP {
				s.push(a)
				s.push(a)
			}

		case NOP:
			// nothing to do
		default:
			return errIllegalOperation
		}
	}

	return nil
}

var (
	errDivideByZero      = errors.New("divide by zero")
	errIllegalOperation  = errors.New("illegal operation")
	errSyntaxError       = errors.New("syntax error")
	errUndefinedVariable = errors.New("undefined variable")
)

// stack represents a simple stack data structure.
type stack struct {
	data  *[]int
	push  func(int)
	pop   func() int
	len   func() int
	empty func() bool
	trail func() []int
}

// newStack creates a new instance of stack.
// This implementation is only suitable here.
func newStack(cap int) *stack {
	data := make([]int, 0, cap)

	return &stack{
		data: &data,
		push: func(i int) { data = append(data, i) },
		pop: func() int {
			top := data[len(data)-1]
			data = data[:len(data)-1]
			return top
		},
		len:   func() int { return len(data) },
		empty: func() bool { return len(data) == 0 },
		trail: func() []int { return data },
	}
}
