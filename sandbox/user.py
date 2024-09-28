import threading
import socket
def startSocket(yourSocket):
    print("hi")
    s = socket.socket()
    s.bind(("localhost", yourSocket))
    s.listen(1)
    c,a = s.accept()
    filetodown = open("receive.png", "wb")
    while True:
        print("Receiving....")
        data = c.recv(1024)
        if data == b"DONE":
           print("Done Receiving.")
           break
        filetodown.write(data)
    filetodown.close()
    filetodown.close()
    c.shutdown(2)
    c.close()
    s.close()

def requestFile(filename, sock):
    s = socket.socket()
    s.connect(("localhost", sock))
    filetosend = open(filename, "rb")
    data = filetosend.read(1024)
    while data:
        print("Sending...")
        s.send(data)
        data = filetosend.read(1024)
    filetosend.close()
    s.send(b"DONE")
    print("Done Sending.")
    print(s.recv(1024))
    s.shutdown(2)
    s.close()

#following is temporary for the time being and should be removed
yourSocket = int(input("your socket number: "))

t1 = threading.Thread(target=startSocket, args=(yourSocket,),name='t1')
t1.start()
while True:
    userInput = input("type in requested filename:")
    if (userInput == ""):
        continue
    if (userInput == " "):
        continue
    if (userInput == "q"):
        break
    
    #TODO request to tracker for socket
    
    #temporary solution to no tracker
    targetSocket = int(input("type in requested socket:"))
    #temp end
    
    sock = 5000
    requestFile(userInput,targetSocket)
    #t2 = threading.Thread(target=requestFile, args=(userInput,sock))

    