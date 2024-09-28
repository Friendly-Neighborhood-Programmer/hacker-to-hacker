from structures import FileByteStream
#def openDownloadSocket():
#    pass

#The following is the function that will be called when a request thread is made
def request_data(self, fileName):
    pass

def writeToFile(self,fileName,fileData):
    fileToDownload = open("/files/"+fileName, "wb")
    File = FileByteStream(fileData)
    for i in range(0,(File.size/File.chunk_size)):
        fileToDownload.write(File.chunks[i])
    fileToDownload.close()

class RequestMessage:
    def __init__(self, file, chunks):
        self.file = file
        self.chunks = chunks