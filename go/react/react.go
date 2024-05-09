// from @eraserix
package react

type cell struct{ value int }

func (c *cell) Value() int {
	return c.value
}

type input struct {
	cell
	reactor *reactor
}

func (c *input) SetValue(v int) {
	if v == c.value {
		return
	}
	c.value = v
	c.reactor.react()
}

type callback struct{ source *compute }

type compute struct {
	cell
	fun func() int
	cbs map[*callback]func(int)
}

func (c *compute) AddCallback(fun func(int)) Canceler {
	cb := &callback{c}
	c.cbs[cb] = fun
	return cb
}

func (c *compute) update() bool {
	old := c.value
	c.value = c.fun()
	return old != c.value
}

func (c *compute) callback() {
	for _, cb := range c.cbs {
		cb(c.value)
	}
}

func (s *callback) Cancel() {
	delete(s.source.cbs, s)
}

type reactor struct {
	dynamics []*compute
}

func New() Reactor {
	return new(reactor)
}

func (r *reactor) CreateInput(v int) InputCell {
	in := &input{reactor: r}
	in.value = v
	return in
}

func (r *reactor) CreateCompute1(dep Cell, fun1 func(int) int) ComputeCell {
	return r.newCompute(func() int { return fun1(dep.Value()) })
}

func (r *reactor) CreateCompute2(dep1 Cell, dep2 Cell, fun2 func(int, int) int) ComputeCell {
	return r.newCompute(func() int { return fun2(dep1.Value(), dep2.Value()) })
}

func (r *reactor) newCompute(fun func() int) ComputeCell {
	cell := &compute{
		fun: fun,
		cbs: make(map[*callback]func(int)),
	}
	cell.value = fun()
	r.dynamics = append(r.dynamics, cell)
	return cell
}

func (r *reactor) react() {
	for _, c := range r.dynamics {
		if c.update() {
			c.callback()
		}
	}
}
