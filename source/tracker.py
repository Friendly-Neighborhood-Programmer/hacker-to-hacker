from socket import socket
import threading
import structures

#For storage have one dict that has keys of ips, values of users
#one dict that has keys of files and and values of users
#For removing user from network, use first dict to find which files they have
#use that to remove them from other dict

files = {}
users = {}

#Handle file resquests through a socket
def requestSocket(portNumber):
    print("File requests socket is open")
    s = socket()
    s.bind(('localhost', portNumber))
    s.listen(1)
    c, a = s.accept()
    
    ip = c.recv(256)
    #Accept ip, then list of files
    usrFiles = c.recv(2048)
    
    # file1 = structures.File("file1", 0, 2048, 512)
    
    # file2 = structures.File("file2", 0, 2048, 512)
    
    # file3 = structures.File("file3", 0, 2048, 512)
    
    # ip = "12.34.567"
    
    # usrFiles = [file1, file2, file3]
    
    #send through ip and files
    users.update({ip:usrFiles})
    
    #Add user to each file
    for file in usrFiles:
        if files.keys().__contains__(file.name):
            newIps = files[file.name]
            newIps.append(ip)
            files.update({file.name: newIps})
        else:
            newList = [ip]
            files.update({file.name: newList})
        
    print(files)
    
    

#Handle maintenance signals through threaded socket