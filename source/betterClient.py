from download import request_data
import threading
from threading import Lock
from structures import FileByteStream

networkFiles = {}
networkFilesLock = Lock()

def main():
    #TODO start daniels thread code
    while True:
        global networkFilesLock
        networkFilesLock.acquire()
        print("These are the availible files: ")
        for key, value in networkFiles.tems():
            print(FileByteStream(key).name)
        networkFilesLock.release()
        
        fileName = input("Which file would you like to download? or type q to quit: ")
        if (fileName == 'q'):
            break
        newThread = threading.Thread(target=request_data, args=(fileName))
        newThread.daemon = True
        newThread.start()