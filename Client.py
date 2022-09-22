# Python program to implement client side of chat room.
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:

    print("Correct usage: script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

def messageCheck(message): # ensures that the message that the user attempts to send is valid

    if len(message) <=0:
        return False
    elif message.isspace():
        return False
    
    return True

while True: 
    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]
                           
    read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])
                                                                
    for socks in read_sockets:
        if socks == server: # if the socket is the server, read the incoming info
            message = socks.recv(2048)
            print (message)
        else: # else read what the user wrote
            message = sys.stdin.readline()
            
            if messageCheck(message): 
                server.send(message)
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()

server.close()
