import socket
import structures
import pickle as pkl
from datetime import datetime
from datetime import timedelta
import threading
from threading import Lock
import time

#For storage have one dict that has keys of ips, values of users
#one dict that has keys of files and and values of users
#For removing user from network, use first dict to find which files they have
#use that to remove them from other dict

files = {}
users = {}
userTimestamps = {}
timestampsLock = Lock()
userTimeoutLength = timedelta(seconds=30)


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

#Handle maintenance signals through threaded socket
def connectSocket(portNumber):
    print("File requests socket is open")
    s = socket.socket()
    s.bind((getLANIP(), portNumber))
    while True:
        s.listen(1)
        
        c, a = s.accept()
        
        #Need ip, port, list of filenames and sizes
        #will be recieving User object
        userData = b''
        while True:
            data = c.recv(512)
            print(data)
            if data == b"DONE":
                print("All data recieved")
                break
            userData += (data)
            
        
        acceptedUser = structures.User.deserialize(userData)
        print(acceptedUser.ip)
        print(acceptedUser.port)
        for file in acceptedUser.files:
            print(file.name, file.size)
        
        
        #send through ip and files
        users.update({acceptedUser.ip:acceptedUser.files})
        print(users)
        
        #Add user to each file
        for file in acceptedUser.files:
            if files.keys().__contains__(file.name):
                newIps = files[file.name][1]
                if newIps.__contains__((acceptedUser.ip, acceptedUser.port)):
                    continue
                newIps.append((acceptedUser.ip, acceptedUser.port))
                files.update({file.name: (file.size, newIps)})
            else:
                newList = [(acceptedUser.ip, acceptedUser.port)]
                files.update({file.name: (file.size, newList)})
        
        global timestampsLock
        timestampsLock.acquire()
        global userTimestamps    
        #Update user's timestamp
        userTimestamps.update({acceptedUser.ip:datetime.now()})
        timestampsLock.release()
            
        #Send all files on the network back to the client
        print(files)
        networkFiles = pkl.dumps(files)
        
        chunkSize = 512
        for i in range(0, len(networkFiles), chunkSize):
            chunk = networkFiles[i:min(i+chunkSize, len(networkFiles))]
            c.send(chunk)
        c.close()

def disconnectUsers():
    #Check every 30 seconds for inacitve users
    while True:
        global timestampsLock
        timestampsLock.acquire()
        print("Disconnect unlocked")
        global userTimestamps
        for user in userTimestamps:
            if (userTimestamps[user] + userTimeoutLength) < datetime.now():
                #Remove the user from the network
                print("Removed: " + user)
                for file in users[user].files:
                    files[file].remove(user)
        timestampsLock.release()
        time.sleep(15)

# userTimestamps.update({"12.345":datetime.now()})

def testLock():
    while True:
        global timestampsLock
        timestampsLock.acquire()
        global userTimestamps
        print(userTimestamps)
        timestampsLock.release()
        time.sleep(5)

if __name__ == "__main__":
    try:
        newThread = threading.Thread(target=disconnectUsers, args=())
        newThread.daemon = True
        newThread.start()
        testLock()
        # connectSocket(50000)
    except KeyboardInterrupt:
        print("override")
