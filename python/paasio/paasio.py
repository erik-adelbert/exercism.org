import io


class MeteredFile(io.BufferedRandom):
    """Implement using a subclassing model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._read_bytes = 0
        self._read_ops = 0
        self._write_bytes = 0
        self._write_ops = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super().__exit__(exc_type, exc_val, exc_tb)

    def __iter__(self):
        return self

    def __next__(self):
        line = super().readline()
        self._read_bytes += len(line)
        self._read_ops += 1

        if line:
            return line
        raise StopIteration

    def read(self, size=-1):
        data = super().read(size)
        self._read_bytes += len(data)
        self._read_ops += 1

        return data

    @property
    def read_bytes(self):
        """read bytes"""
        return self._read_bytes

    @property
    def read_ops(self):
        """read ops"""
        return self._read_ops

    def write(self, b):
        nbytes = super().write(b)
        self._write_bytes += nbytes
        self._write_ops += 1

        return nbytes

    @property
    def write_bytes(self):
        """write bytes"""
        return self._write_bytes

    @property
    def write_ops(self):
        """write ops"""
        return self._write_ops


class MeteredSocket:
    """Implement using a delegation model."""

    def __init__(self, socket):
        self.socket = socket

        self._recv_bytes = 0
        self._recv_ops = 0
        self._send_bytes = 0
        self._send_ops = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.socket.__exit__(exc_type, exc_val, exc_tb)

    def recv(self, bufsize, flags=0):
        """recv"""
        data = self.socket.recv(bufsize, flags)
        self._recv_bytes += len(data)
        self._recv_ops += 1

        return data

    @property
    def recv_bytes(self):
        """recv_bytes"""
        return self._recv_bytes

    @property
    def recv_ops(self):
        """recv_ops"""
        return self._recv_ops

    def send(self, data, flags=0):
        """send"""
        nbytes = self.socket.send(data, flags)
        self._send_bytes += nbytes
        self._send_ops += 1

        return nbytes

    @property
    def send_bytes(self):
        """send bytes"""
        return self._send_bytes

    @property
    def send_ops(self):
        """send ops"""
        return self._send_ops
