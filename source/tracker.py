import socket
import structures
import pickle as pkl
from datetime import datetime

#For storage have one dict that has keys of ips, values of users
#one dict that has keys of files and and values of users
#For removing user from network, use first dict to find which files they have
#use that to remove them from other dict

files = {}
users = {}
userTimestamps = {}
timeoutLength = 30
datetime.second

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
            newIps = files[file.name]
            newIps.append((acceptedUser.ip, acceptedUser.port))
            files.update({file.name: (file.size, newIps)})
        else:
            newList = [(acceptedUser.ip, acceptedUser.port)]
            files.update({file.name: (file.size, newList)})
        
    #Update user's timestamp
    
        
    #Send all files on the network back to the client
    print(files)
    networkFiles = pkl.dumps(files)
    
    chunkSize = 512
    for i in range(0, len(networkFiles), chunkSize):
        chunk = networkFiles[i:min(i+chunkSize, len(networkFiles))]
        c.send(chunk)

def disconnectUsers():
    #Check every so often for inacitve users
    for user in userTimestamps:
        if (datetime.now() - userTimestamps[user]).total_seconds() < 30:
            #Remove the user from the network
            print(user)

try:
    connectSocket(50000)
except KeyboardInterrupt:
    print("override")
