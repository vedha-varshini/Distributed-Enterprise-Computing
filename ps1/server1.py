import socket
import threading

# Function to handle clients' connections
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received message: {message}")
            broadcast(message, client_socket)
        except:
            client_socket.close()
            break

# Function to broadcast messages to all clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

# Main server code
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5555))
server.listen(5)

print("Server started, waiting for connections...")

clients = []

while True:
    client_socket, addr = server.accept()
    print(f"New connection from {addr}")
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket,)).start()
