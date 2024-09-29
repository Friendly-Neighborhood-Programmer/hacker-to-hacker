import socket
import structures
import pickle as pkl
from datetime import datetime
from datetime import timedelta
import threading
from threading import Lock
import time


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
    
    print("Connect socket")
    while True:
        s.listen(1)
        
        c, a = s.accept()
        
        userData = b''
        while True:
            data = c.recv(512)
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
        print(userTimestamps)
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
        global files
        global userTimestamps
        removedUsers = []
        for user in userTimestamps:
            if (userTimestamps[user] + userTimeoutLength) < datetime.now():
                #Remove the user from the network
                print("Removed: " + user)
                for file in users[user]:
                    print(files[file.name])
                    
                    updatedUsers = []
                    for socket in files[file.name][1]:
                        if socket[0] != user:
                            updatedUsers.append(socket)
                            
                    files[file.name] = (files[file.name][0], updatedUsers)
                    if (len(files[file.name][1]) == 0):
                        print("No users have " + file.name)
                        del files[file.name]
                
                removedUsers.append(user)
                del users[user]
        for removed in removedUsers:
            del userTimestamps[removed]
        print(files)
        print(users)
        print(userTimestamps)
        timestampsLock.release()
        time.sleep(10)

if __name__ == "__main__":
    try:
        newThread = threading.Thread(target=disconnectUsers, args=())
        newThread.daemon = True
        newThread.start()
        connectSocket(50000)
    except KeyboardInterrupt:
        print("override")
