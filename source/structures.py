import pickle as pkl

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


class FileChunk:
    def __init__(self, index, size, hash, data):
        self.index = index
        self.size = size
        self.hash = hash # todo implement hash later
        self.data = data

    def serialize(self):
        return pkl.dumps(self)

    def deserialize(chunkData):
        return pkl.loads(data)
