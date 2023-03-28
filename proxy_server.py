# Import socket module
from socket import *    

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

proxySocket = socket(AF_INET, SOCK_STREAM)

proxyPort = 8888
proxySocket.bind(('', proxyPort))

proxySocket.listen(10)

while True:
    print('Proxy Server Ready...\n')

    connectionSocket, addr = proxySocket.accept() 

    try:

        message = connectionSocket.recv(10240).decode() 
        if not message:
            continue
        
        print("\t--- Message Content ---")
        print(message)
        print("\t--- End of Message Content ---\n")

        print("\t--- File Content ---")
        filenameProxy = message.split()[1]
        if(filenameProxy == '/favicon.ico'):
            print("err")
            continue
        filename = filenameProxy.split('/')[2]
        #print("Filename: " + filename)
        index = filename.rfind('.')
        filetype = filename[index+1:len(filename)]
        #print("Filetype: " + filetype)
        #print("\t--- End of File Content ---\n")
        fileCached = "false"
        if(filetype == 'html' or filetype == 'txt'):
            f = open("proxy_" + filename, encoding='utf-8')
            print("File found in cache")
            fileCached = "true"
            outputdata = f.read()  
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            connectionSocket.sendall(outputdata.encode())
            
        elif(filetype == "jpg" or filetype == "jpeg" or filetype == 'png'):
            f = open("proxy_" + filename, "rb")
            print("File found in cache")
            fileCached = "true"
            outputdata = f.read()
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            connectionSocket.sendall(outputdata)
            
        else:
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            

        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        
        if(fileCached == "false"):
            serverSocket = socket(AF_INET, SOCK_STREAM)
                
            print(addr[0])
            serverSocket.connect((addr[0],6789))

            webReq = "GET /" + filename + " HTTP/1.1\n"
            serverSocket.send(webReq.encode())
            if(filetype == "html" or filetype == "txt"):
                print("File not found in cache")
                webHeader = serverSocket.recv(1024).decode() #receives HTTP response header
                webMsg = serverSocket.recv(10240).decode() #receives HTTP message
                webMsgAll = webMsg
                while webMsg:
                    webMsg = serverSocket.recv(10240).decode()
                    webMsgAll = webMsgAll + webMsg
                print("Response from Web Server: " + str(webMsgAll))
                if(webMsg == "HTTP/1.1 404 Not Found\r\n\r\n"):
                    print("No file exists")
                    connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                    connectionSocket.close()
                    continue
                filename_name = filename
                cachedFile = open("proxy_" + filename_name, "w+")
                cachedFile.writelines(webMsgAll)

                cachedFile.close()

                readFile = open("proxy_" + filename_name)
                outdata = readFile.read()

                readFile.close()
                connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                connectionSocket.sendall(outdata.encode())
                
            elif(filetype == "jpg" or filetype == "jpeg" or filetype == 'png'):
                print("File not found in cache")
                webHeader = serverSocket.recv(1024).decode() #receives HTTP response header
                webMsg = serverSocket.recv(10240)
                webMsgAll = webMsg
                while webMsg:
                    webMsg = serverSocket.recv(10240)
                    webMsgAll = webMsgAll + webMsg
                if(webMsgAll == "HTTP/1.1 404 Not Found\r\n\r\n"):
                    print("No file exists")
                    connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                    connectionSocket.close()
                    continue
                filename_name = filename
                cachedFile = open("proxy_" + filename_name, "wb")
                cachedFile.write(webMsgAll)
                cachedFile.close()


                readFile = open("proxy_" + filename_name, "rb")
                outdata = readFile.read()

                
                readFile.close()
                connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                connectionSocket.sendall(outdata)

            serverSocket.close()
        
            connectionSocket.close()

        else:
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            connectionSocket.close()


serverSocket.close()  
