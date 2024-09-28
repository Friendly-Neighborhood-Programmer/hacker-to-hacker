from socket import socket

def openUploadSocket(self, portNumber):
    # todo remove debug print
    print("upload socket has opened on port", portNumber)
    s = socket()
    s.bind(('localhost', portNumber))
    s.listen(1)
    c, a = s.accept()
    fileName = c.recv(1024)
    fileName = fileName.decode()
    print(fileName)

    try:
        fileToSend = open(fileName, "rb")
        data = fileToSend.read(1024)
        while data:
            c.send(data)
            data = fileToSend.read(1024)
        fileToSend.close()
        print("Done Sending.")
        #print(s.recv(1024))
        c.shutdown(2)
        c.close()

    except Exception as e:
        c.shutdown(2)
        c.close()

def send_data(self, file):
    pass