import socket
import threading

# Function to handle receiving messages
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received message: {message}")
        except:
            client_socket.close()
            break

# Main client code
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 5555))

print("Connected to the chat server.")

threading.Thread(target=receive_messages, args=(client_socket,)).start()

while True:
    message = input()
    client_socket.send(message.encode('utf-8'))
