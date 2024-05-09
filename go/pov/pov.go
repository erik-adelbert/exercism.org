package pov

import "slices"

// Tree represents a tree-like data structure.
type Tree struct {
	value    string
	children []*Tree
}

// New creates and returns a new Tree with the given root value and children.
func New(value string, children ...*Tree) *Tree {
	return &Tree{
		value:    value,
		children: children,
	}
}

// Value returns the value at the root of a tree.
func (tr *Tree) Value() string {
	return tr.value
}

// Children returns a slice containing the children of a tree.
// There is no need to sort the elements in the result slice,
// they can be in any order.
func (tr *Tree) Children() []*Tree {
	return tr.children
}

// addChild adds a child node to the current node.
func (tr *Tree) addChild(c *Tree) {
	tr.children = append(tr.children, c)
}

// delChild deletes a child node from the current node.
func (tr *Tree) delChild(c *Tree) {
	last := len(tr.children) - 1
	if i := slices.Index(tr.children, c); i >= 0 {
		tr.children[i] = tr.children[last]
		tr.children = tr.children[:last]
	}
}

// POV problem-specific functions

// mapPathToRoot traverses the tree from the root to the specified node 'from'.
// It applies the provided function 'fun' backward to each node in the path.
func (tr *Tree) mapPathToRoot(from string, fun func(cur, nxt *Tree)) *Tree {

	// Stack to perform DFS traversal
	stack := newStack()

	path := make(map[*Tree]*Tree)
	path[tr] = nil

	root := tr
	stack.push(root)

	// Perform DFS traversal
	for !stack.empty() {
		root = stack.pop()
		if root.value == from {
			goto FOUND
		}
		for _, c := range root.children {
			path[c] = root
			stack.push(c)
		}
	}
	return nil // not found

FOUND:
	// update tree upto initial root
	cur, nxt := root, root
	for {
		cur = nxt
		if nxt = path[cur]; nxt == nil {
			break
		}
		fun(cur, nxt)
	}

	return root
}

// FromPov balances the tree to be rooted at the node specified in the argument.
// It returns the node 'from' which is the new root or nil if 'from' is not found.
func (tr *Tree) FromPov(from string) *Tree {

	// Check for corner cases
	switch {
	case tr == nil:
		return nil
	case tr.value == from:
		// nothing to do
		return tr
	case len(tr.children) == 0:
		// singleton with bad request
		return nil
	}

	// Fixup the tree such as 'from' is promoted to the root
	return tr.mapPathToRoot(from, func(cur, nxt *Tree) {
		// reverse link along the path
		nxt.delChild(cur)
		cur.addChild(nxt)
	})

}

// PathTo returns the shortest path between two nodes in the tree.
func (tr *Tree) PathTo(from, to string) []string {

	// Balance the tree to promote 'to' as the root
	if tr = tr.FromPov(to); tr == nil {
		// 'to' not found
		return nil
	}

	// captured buffer
	var out = []string{from}

	// Output the path while browsing 'from' -> 'to'
	found := tr.mapPathToRoot(from, func(_, nxt *Tree) {
		// push node names in LIFO order to the out buffer
		out = append(out, nxt.value) // capture out
	})
	if found == nil {
		// 'from' not found
		return nil
	}

	return out
}

// stack represents a simple stack data structure.
type stack struct {
	data  *[]*Tree
	push  func(*Tree)
	pop   func() *Tree
	empty func() bool
}

// newStack creates a new instance of stack.
// This implementation is only suitable here.
func newStack() *stack {
	var data []*Tree

	return &stack{
		data: &data,
		push: func(tr *Tree) { data = append(data, tr) },
		pop: func() *Tree {
			top := data[len(data)-1]
			data = data[:len(data)-1]
			return top
		},
		empty: func() bool { return len(data) == 0 },
	}
}

// String describes a tree in a compact S-expression format.
// This helps to make test outputs more readable.
// Feel free to adapt this method as you see fit.
// func (tr *Tree) String() string {
// 	if tr == nil {
// 		return "nil"
// 	}
// 	result := tr.Value()
// 	if len(tr.Children()) == 0 {
// 		return result
// 	}

// 	for _, ch := range tr.Children() {
// 		result += " " + ch.String()
// 	}
// 	return "(" + result + ")"
// }
