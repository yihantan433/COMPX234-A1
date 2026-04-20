#server.py
#tcpprogram created by Yihan Tan .4.20
#Server
import socket

#Create a socket object,AF_INET=用IPv4地址；SOCK_STREAM=用TCP协议
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to my machine and port
server_socket.bind("0.0.0.0",51234)
#Start listening,allowing up to 5 connections
server_socket.listen(5)
print("Server is listening on port 51234...")
#Stuck in an infinite loop,waiting for clients to connect
while True:
    #Accept a connection from a client
    client_socket, addr = server_socket.accept()
    print("Accepted connection from", addr)
    #Receive data from the client
    data = client_socket.recv(1024)
    text = data.decode("utf-8")
    print(f"Message from {addr}: {text}")
    #Reply to the client
    reply = "received your message: "
    client_socket.sendall(reply)
    #close the client socket
    client_socket.close()
    server_socket.close()
    print("Server closed")
