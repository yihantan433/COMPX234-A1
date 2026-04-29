import socket
import sys
import os

def main():
    if len(sys.argv) != 4:
        print("Usage: python tuple_space_client.py <server-hostname> <server-port> <input-file>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    input_file_path = sys.argv[3]

    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' does not exist.")
        sys.exit(1)

    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # TASK 1: Create a TCP/IP socket and connect it to the server.
    # Hint: socket.socket(socket.AF_INET, socket.SOCK_STREAM) creates the socket.
    # Then call sock.connect((hostname, port)) to connect.
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((hostname,port))


    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" ", 2)
            cmd = parts[0]
            message = ""

            # TASK 2: Build the protocol message string to send to the server.
            # Format:  "NNN X key"        for READ / GET
            #          "NNN P key value"   for PUT
            # where NNN is the total message length as a zero-padded 3-digit number,
            # X is "R" for READ and "G" for GET.
            # Hint: for READ/GET, size = 6 + len(key). For PUT, size = 7 + len(key) + len(value).
            # Reject lines with invalid format or key+" "+value > 970 chars.
            if cmd == "READ":
                key = parts[1]
                body = f"R {key}"
                size = len(body) + 3  
                message = f"{size:03d}{body}"
             elif cmd == "GET":
             elif cmd == "PUT":
                key = parts[1]
              value = parts[2]  
              body = f"P {key} {value}"
             size = len(body) + 3
             message = f"{size:03d}{body}"
else:
            # TASK 3: Send the message to the server, then receive the response.
            # - Send:    sock.sendall(message.encode())
            # - Receive: first read 3 bytes to get the response size (like the server does).
            #            Then read the remaining (size - 3) bytes to get the response body.
    # 收长度头
            len_bytes = receive_n(sock, 3)  
            resp_size = int(len_bytes.decode())
            resp_body = b""
            while len(resp_body) < resp_size - 3:
            chunk = sock.recv(resp_size - 3 - len(resp_body))
              if not chunk:
                   break
            resp_body += chunk
            response_buffer = resp_body

            response = response_buffer.decode().strip()
            print(f"{line}: {response}")

    except (socket.error, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        # TASK 4: Close the socket when done (already called for you — explain why
        #finally: is the correct location because it guarantees sock.close() 
        #executes under all exit conditions — normal completion, continue, or any exception (e.g., recv() failure, server disconnection). 
        #Without it, an early continue or unhandled error would skip the cleanup, 
        #resulting in a socket leak where the operating system keeps the port occupied by a stale connection.
        # finally: is the right place to do this even if an error occurs above).
        sock.close()

if __name__ == "__main__":
    main()