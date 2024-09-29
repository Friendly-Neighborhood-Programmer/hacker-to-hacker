import socket
import hashlib
from structures import FileChunk, RequestMessage
from tracker import getLANIP

def openUploadSocket(portNumber, ip):
    s = socket.socket()
    s.bind((ip, portNumber))
    s.listen(4)
    return s

def send_data(c, fileName, chunkSet):
    try:
        print(chunkSet)
        with open(f'../files/{fileName}', 'rb') as upFile:
            index = 0 + chunkSet[0]
            chunkRange = chunkSet[-1] - chunkSet[0]
            #upFile.seek(chunkSet[0] * 256)
            upFile.seek(chunkSet[0] * 512)

            while index < chunkRange + chunkSet[0]:
                data = upFile.read(512)
                #data = upFile.read(256)
                #wrapper = FileChunk(index, 256, data)

                #c.send(wrapper.serialize())
                c.send(data)
                index = index + 1

            c.shutdown(2)
            c.close()

    except Exception as e:
        print(e)
        c.shutdown(2)
        c.close()

def awaitUploadRequest(ip,port):
    # debug
    #s = openUploadSocket(50001, "localhost")
    #s = openUploadSocket(50001, getLANIP())
    s = openUploadSocket(port, ip)
    while True:
        connection, address = s.accept()
        messageBytes = connection.recv(512)
        requestMessage = RequestMessage.deserialize(messageBytes)
        send_data(connection, requestMessage.fileName, requestMessage.chunks)

def hashData(data):
    # h = hashlib.blake2b()
    # h.update(data)
    # return h.hexdigest()
    return data