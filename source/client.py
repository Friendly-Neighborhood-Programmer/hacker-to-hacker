import threading
import socket
from structures import FileByteStream, User
import os
import pickle as pkl
from threading import Lock
from download import completeFileRequest
from time import sleep
from seeding import awaitUploadRequest

networkFiles = {}
networkFilesLock = Lock()

LOCAL_UPLOAD_PORT = 50001
LOCAL_IP = None

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

def processFilesInFolder(folder_path):
    fileByteStreams = []

    # Traverse through all files in the folder
    for root, dir, files in os.walk(folder_path):
        for fileName in files:
            filePath = os.path.join(root, fileName)
            
            # Get the file size
            fileSize = os.path.getsize(filePath)
            
            # Compute the file hash
            fileHash = fileName
            
            # Create a FileByteStream instance for this file
            fileByteStream = FileByteStream(fileName, fileHash, fileSize)

            # Append the completed FileByteStream to the list
            fileByteStreams.append(fileByteStream)
    
    return fileByteStreams

# TODO set values
TRACKER_IP = '192.168.27.76'
TRACKER_PORT = 50000

def pingTracker():
    s = socket.socket()
    #s.bind('localhost', 42069)
    s.connect((TRACKER_IP, TRACKER_PORT))
    
    user = User(getLANIP())
    user.port = LOCAL_UPLOAD_PORT
    #get all files
    user.files = processFilesInFolder('../files')
    serializedUser = user.serialize()

    chunkSize = 512
    for i in range(0, len(serializedUser), chunkSize):
        chunk = serializedUser[i : min(i + chunkSize, len(serializedUser))]
        s.send(chunk)

    s.send(b'DONE')
    try:
        currentNetworkFiles = b''
        while True:
            data = s.recv(512)
            if not data:
                # print("Connection Closed.")
                # print("Finished Receiving Network Files.")
                break
            currentNetworkFiles += data
        
        global networkFilesLock
        networkFilesLock.acquire()
        global networkFiles
        networkFiles = pkl.loads(currentNetworkFiles)
        networkFilesLock.release()

        s.close()
    except:
        s.close()
    
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

def testing():
    try:
        pingTracker()
        #following is temporary for the time being and should be removed
        LOCAL_UPLOAD_PORT = int(input("Fnter your upload socket number: "))

        # t1 = threading.Thread(target=uploadSocket, args=(LOCAL_UPLOAD_PORT,),name='t1')
        # t1.daemon = True
        # t1.start()
        # #userInput = input("type in requested filename:")
        # userInput = '../files/tosend.png'
        # if (userInput == ""):
        #     ...
        # if (userInput == " "):
        #     ...
        # if (userInput == "q"):
        #     ...
        # #TODO request to tracker for socket
                
        # #temporary solution to no tracker
        # targetSocketNumber = int(input("type in requested socket:"))
        # #temp end
            
        # downloadSocketNumber = int(input('Enter your download socket:'))
        # requestFile(userInput, targetSocketNumber, downloadSocketNumber)
        # #t2 = threading.Thread(target=requestFile, args=(userInput,sock))

    except KeyboardInterrupt:
        #run override code
        print("override")

def loopPing():
    global networkFiles
    while True:
        pingTracker()
        sleep(10)

def main():
    global networkFiles
    #TODO start daniels thread code
    pingServer = threading.Thread(target=loopPing, args=())
    pingServer.daemon = True
    pingServer.start()
    LOCAL_IP = getLANIP()
    t1 = threading.Thread(target=awaitUploadRequest,args=(LOCAL_IP,LOCAL_UPLOAD_PORT))
    t1.daemon = True
    t1.start()

    print("\nWelcome to the Hacker-to-Hacker Network, a file sharing service for hackers around the world!\n")

    while True:
        ### add status to network before start
        
        userInput = promptUser()
        match userInput:
            case "1":
                global networkFilesLock
                networkFilesLock.acquire()
                prettyPrint(networkFiles)
                networkFilesLock.release()
                continue

            case "2":
                fileName = input("Name of the file you would like to download: ")
                networkFilesLock.acquire()
                if not fileName in networkFiles:
                    print("File not found on the Hacker Network, enter the name of a valid file\n")
                    continue

                newThread = threading.Thread(target=completeFileRequest, args=(fileName, networkFiles[fileName]))
                newThread.daemon = True
                newThread.start()
                newThread.join() # maybe this will allow multiple at once?
                networkFilesLock.release()
                continue

            case "q":
                print("Leaving the Hacker Network...")
                break

            case _:
                print("Please enter a valid option\n")
                continue

    exit()

def promptUser():
    return input("Here are your options:\n" \
        "(1) View files available on the network.\n" \
        "(2) Begin download of a file.\n" \
        "(q) to to quit.\n")

def prettyPrint(networkFiles):  
    print("Files available for download:")
    for key, value in networkFiles.items():
        print(f"File: {key}")
        print(f"Size: {value[0]} bytes")
        print(f"Sources ({len(value[1])}):")
        for owner in value[1]:
            print(f"{owner[0]}:{owner[1]}")
        print("\n")

if __name__ == '__main__':
    main()