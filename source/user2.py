from seeding import *
from download import *
from struct import *
from client import *

try:
    if input("Do you want to seed? (y/n): ") == 'y':
        awaitUploadRequest()
    else:
        pingTracker()
        

except KeyboardInterrupt:
    #run override code
    print("override")