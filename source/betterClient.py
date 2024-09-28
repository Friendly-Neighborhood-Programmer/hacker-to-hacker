from download import request_data
import threading
from threading import Lock
from structures import FileByteStream

networkFileData =[]
networkFileDataLock = Lock()

def main():
    #TODO start daniels thread code
    while True:

        networkFileDataLock.acquire()
        print("These are the availible files: ")
        for file in networkFileData:
            print(FileByteStream(file).name)
        networkFileDataLock.release()
        
        fileName = input("Which file would you like to download? or type q to quit: ")
        if (fileName == 'q'):
            break
        newThread = threading.Thread(target=request_data, args=(fileName))
        newThread.daemon = True
        newThread.start()