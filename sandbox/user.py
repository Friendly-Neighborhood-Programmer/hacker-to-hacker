import threading
from socket import socket

def uploadSocket(portNumber):
    print("Send socket has been opened.")
    s = socket()
    s.bind(('192.168.27.76', portNumber))
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
        c.shutdown(2)
        c.close()

    except Exception as e:
        print(e)
        c.shutdown(2)
        c.close()
    
def requestFile(fileName, targetPortNumber, downloadPortNumber):
    s = socket()
    s.bind(('localhost', downloadPortNumber))
    s.connect(('localhost', targetPortNumber))
    s.send(fileName.encode())

    try:
        fileToDownload = open("../files/receive.png", "wb")
        while True:
            data = s.recv(1024)
            if not data:
                print("Connection Closed.")
                print("Finished Receiving.")
                break
            fileToDownload.write(data)

        fileToDownload.close()
        s.close()
    except:
        s.close()

try:
    #following is temporary for the time being and should be removed
    uploadSocketNumber = int(input("Fnter your upload socket number: "))


    t1 = threading.Thread(target=uploadSocket, args=(uploadSocketNumber,),name='t1')
    t1.daemon = True
    t1.start()
    #userInput = input("type in requested filename:")
    userInput = '../files/tosend.png'
    if (userInput == ""):
        ...
    if (userInput == " "):
        ...
    if (userInput == "q"):
        ...
        
            
    #TODO request to tracker for socket
            
    #temporary solution to no tracker
    targetSocketNumber = int(input("type in requested socket:"))
    #temp end
        
    downloadSocketNumber = int(input('Enter your download socket:'))
    requestFile(userInput, targetSocketNumber, downloadSocketNumber)
    #t2 = threading.Thread(target=requestFile, args=(userInput,sock))

except KeyboardInterrupt:
    #run override code
    print("override")