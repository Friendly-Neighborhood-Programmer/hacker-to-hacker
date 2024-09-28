import threading
import socket
from structures import FileByteStream, User

LOCAL_UPLOAD_PORT = None
LOCAL_IP = None

def uploadSocket(portNumber):
    print("Send socket has been opened.")
    s = socket.socket()
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

# TODO set values
TRACKER_IP = 0
TRACKER_PORT = 50000

def getLANIP():
    try:
        # Create a socket and connect to a remote server (e.g., Google's DNS)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        
        # Get the LAN IP address
        LANIP = s.getsockname()[0]
        
    except Exception as e:
        print(f"Error getting LAN IP: {e}")
        LANIP = '127.0.0.1'  # Fallback to localhost if there's an issue
    finally:
        s.close()

    return LANIP

def pingTracker():
    s = socket.socket()
    #s.bind('localhost', 42069)
    s.connect(TRACKER_IP, TRACKER_PORT)
    
    user = User()
    user.ip = getLANIP()
    user.port = LOCAL_UPLOAD_PORT
    
    #get all files
    
def requestFile(fileName, targetPortNumber, downloadPortNumber):
    s = socket.socket()
    #s.bind(('localhost', downloadPortNumber))
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
  LOCAL_UPLOAD_PORT = int(input("Fnter your upload socket number: "))

  t1 = threading.Thread(target=uploadSocket, args=(LOCAL_UPLOAD_PORT,),name='t1')
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

    