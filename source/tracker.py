import socket
import threading
import structures

#For storage have one dict that has keys of ips, values of users
#one dict that has keys of files and and values of users
#For removing user from network, use first dict to find which files they have
#use that to remove them from other dict

files = {}
users = {}

#Handle maintenance signals through threaded socket
def connectSocket(portNumber):
    print("File requests socket is open")
    s = socket()
    s.bind(('localhost', portNumber))
    s.listen(1)
    
    
    c, a = s.accept()
    
    #Need ip, port, list of filenames and sizes
    #will be recieving User object
    
    
    acceptedUser = structures.User
    
    #send through ip and files
    users.update({acceptedUser.ip:acceptedUser.files})
    
    #Add user to each file
    for file in acceptedUser.files:
        if files.keys().__contains__(file.name):
            newIps = files[file.name]
            newIps.append(acceptedUser.ip)
            files.update({file.name: newIps})
        else:
            newList = [acceptedUser.ip]
            files.update({file.name: newList})
        
    
        
    print(files)
    
    
#Handle file resquests through a socket

t1 = threading.Thread(target=connectSocket, args=(50000,),name='t1')
t1.daemon = True
t1.start()