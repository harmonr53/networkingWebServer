#import the socket module
from socket import *
import sys #  In order to terminate the program
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a server socket
serverSocket.bind((gethostname(), 13331))
thost = gethostname()
serverSocket.listen()
while True:
  #Establish the connection
  print(f'Ready to serve at {thost} port 13331')
  (connectionSocket, addr) = serverSocket.accept()
  print(addr)
  try:
    bytes_recvd = 0
    # print('Right before the recv')
    message = connectionSocket.recv(2048) #Get http request from the socket
    # print('Right after the recv')
    # print(f'This is the message: {message}')
    filename = message.split()[1]
    # print(f'This is the filename: {filename}')
    f = open(filename[1:])
    outputdata = f.read() #read the contents of helloworld.html
    loutputdata = len(outputdata)
    #Send one HTTP header line into socket
    outputheader = f'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\n\n'
    for i in range(0,len(outputheader)):
      connectionSocket.send(outputheader[i].encode())
    connectionSocket.send("\r\n".encode())
    # print(f'The following header has been sent: \r\n{outputheader}')
    #Send the content of the requested file to the client
    for i in range(0,len(outputdata)):
      connectionSocket.send(outputdata[i].encode())
    connectionSocket.send("\r\n".encode())
    # print(f'The following data has been sent: \r\n{outputdata}')
    connectionSocket.close()
  except:
    #Send response for message for file not found
    # print('Uh oh...were in the exception.')
    outputerror = "HTTP/1.1 404 Not Found"
    for i in range(0,len(outputerror)):
      connectionSocket.send(outputerror[i].encode())
    connectionSocket.send("\r\n".encode())
    #Close client socket
    connectionSocket.close()
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
