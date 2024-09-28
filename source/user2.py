from seeding import *
from download import *
from struct import *
from client import *

try:
    if input("Do you want to seed? (y/n): ") == 'y':
        awaitUploadRequest()
    else:
        pingTracker()
        completeFileRequest("../files/tosend.png", fileInfo)

except KeyboardInterrupt:
    #run override code
    print("override")