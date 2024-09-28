import socket
from structures import FileChunk
def openUploadSocket(self, file, portNumber,ip):
    print("Send socket has been opened.")
    sock = socket()
    sock.bind((ip, portNumber))
    try:
        while True:
            sock.listen(1)
            c = sock.accept()
            fileName = c.recv(512)
            fileName = fileName.decode()
            print("request for: "+fileName)

            
            fileToSend = open(fileName, "rb")
            data = fileToSend.read(256)
            index = 0
            while data:
                wrapper = FileChunk()
                wrapper.data = data
                wrapper.index =index
                wrapper.size = 256
                #wrapper.hash = 

                index = index+1
                c.send(data)
                data = fileToSend.read(256)
                fileToSend.close()
                print("Done Sending.")
                #print(s.recv(1024))
                c.shutdown(2)
                c.close()

    except Exception as e:
        print(e)
        c.shutdown(2)
        c.close()

def send_data(self, file):
    pass