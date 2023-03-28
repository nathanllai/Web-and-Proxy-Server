# Import socket module
from socket import *    

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)


serverPort = 6789
serverSocket.bind(("", serverPort))

serverSocket.listen(1)

while True:
    print('Ready to serve...')

    connectionSocket, addr = serverSocket.accept() 

    try:

        message = connectionSocket.recv(1024).decode() 
        if not message:
            continue
        
        #print(message)

        filename = message.split()[1]
        index = filename.rfind('.')
        filetype = filename[index+1:len(filename)]

        if(filetype == 'html' or filetype == 'txt'):
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            f = open(filename[1:], encoding='utf-8')
            outputdata = f.read()  
            connectionSocket.sendall(outputdata.encode())
        elif(filetype == "jpg" or filetype == "jpeg" or filetype == 'png'):
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            f = open(filename[1:], "rb")
            outputdata = f.read()
            connectionSocket.sendall(outputdata)
        else:
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            

        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:

        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())

        connectionSocket.close()


serverSocket.close()  