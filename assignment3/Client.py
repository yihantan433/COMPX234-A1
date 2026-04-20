import socket
#Create a socket object,AF_INET=用IPv4地址；SOCK_STREAM=用TCP协议
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect to the server
client_socket.connect(("localhost", 51234))
#Send a message to the server
msg = "HAHAHAHAHAHAH"
client_socket.sendall(msg)  
#Receive the server's reply
data = client_socket.recv(1024)
text = data
print(f"Received: {text}")
#Close the socket
client_socket.close()
