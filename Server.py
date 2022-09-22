#https://www.geeksforgeeks.org/simple-chat-room-using-python/ <- used for reference
  
import socket
import select
import sys

from thread import *

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET for correct domain addressing and SOCK_STREAM for continous data
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


IP_address = str(sys.argv[1])
PORT = int(sys.argv[2])

server.bind((IP_address,PORT)) # give server IP and port

server.listen(2)

list_of_clients = []


def remove(conn):

    if conn in list_of_clients:
        list_of_clients.remove(conn)

def broadcast(message,conn): # same kind of code from clientthread but 
    for client in list_of_clients:
        if client != conn:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)

def clientthread(conn,addr): # handles interactions between individual connection (user)

    conn.send("Hello world {}!".format(addr))
    
    while True:
        try:
            message = conn.recv(2048) # max size, im assuming in bytes. ASCII? returns bytes object which suffices a conditional statement (if message exists)
            
            if message: # message has been recieved from user successfully 
                
                send = "<{}>{}".format(addr,message)
                broadcast(send,conn)
            
            else: # message has come back bad, sign of bad connection 
                remove(conn)
        except:
            continue


while True:

    conn, addr = server.accept() # store connection struct and address information from accept function
    list_of_clients.append(conn)

    print(addr[0] + " has connected")

    start_new_thread(clientthread,(conn,addr)) # assuming the function address is needed for memory safety? 

conn.close()
server.close()

