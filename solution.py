#import socket module
from socket import *
import sys # In order to terminate the program

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Prepare a sever socket
    serverSocket.bind((gethostbyname("localhost"), port))
    # print('gethostname: ' + gethostname())
    # print('gethostbyname: ' + gethostbyname("localhost"))
    #Fill in start
    serverSocket.listen()
    #Fill in end

    while True:
        #Establish the connection
        # print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(2048)
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()

            #Send one HTTP header line into socket
            outputheader = "HTTP/1.0 200 OK Content-Type: text/html; charset=UTF-8"
            for i in range(0, len(outputheader)):
                connectionSocket.send(outputheader[i].encode())
            connectionSocket.send("\r\n".encode())

            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())

            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
            # break
        except (IOError, BrokenPipeError) as e:
            #Send response message for file not found (404)
            outputerror = "HTTP/1.0 404 Not Found"
            for i in range(0, len(outputerror)):
                connectionSocket.send(outputerror[i].encode())
            connectionSocket.send("\r\n".encode())

            #Close client socket
            connectionSocket.close()
            pass

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
