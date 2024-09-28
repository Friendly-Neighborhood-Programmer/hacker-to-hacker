class User:
    def __init__(self, ip, port = 5000):
        self.ip
        self.port = port
        self.files = []

    def add_file(self, file):
        pass


class FileByteStream:
    def __init__(self, name, hash, size, chunk_size):
        self.name = name
        self.hash = hash # todo implement hash later
        self.size = size
        self.chunk_size = chunk_size
        self.chunks = {}


class Chunk:
    def __init__(self, index, size, hash):
        self.index = index
        self.size = size
        self.hash = hash # todo implement hash later