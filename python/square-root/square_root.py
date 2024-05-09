def square_root(n):
    if n is None or (not isinstance(n, int)):
        raise TypeError('input must be an integer') # pragma: no cover

    if n < 0:
        raise ValueError('input must be a non-negative integer') # pragma: no cover

    root = 0 # Running result.
    rmdr = 0 # Running remainder ``n - root**2``.
    for s in reversed(range(0, n.bit_length(), 2)): # Shift ``n`` by ``s`` bits.
        bits = n >> s & 3 # The next two most significant bits of ``n``.
        rmdr = rmdr << 2 | bits # Increase the remainder.
        cand = root << 2 | 1 # Shifted candidate root value to try.
        bit_next = int(rmdr >= cand) # The next bit in the remainder.
        root = root << 1 | bit_next # Add next bit to running result.
        rmdr -= cand * bit_next # Reduce the remainder if bit was added.
    return root
