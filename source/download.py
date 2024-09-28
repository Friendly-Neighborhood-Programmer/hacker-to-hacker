from structures import FileByteStream
def openDownloadSocket():
    pass

def request_data(self, file):
    pass

def writeToFile(fileName,fileData):
    fileToDownload = open("/files/"+fileName, "wb")
    File = FileByteStream(fileData)
    for i in range(0,(File.size/File.chunk_size)):
        fileToDownload.write(File.chunks[i])
    fileToDownload.close()

class RequestMessage:
    def __init__(self, file, chunks):
        self.file = file
        self.chunks = chunks