import socket
import threading

# Server Information
HOST = '127.0.0.1'  # localhost
PORT = 12345        # Arbitrary port for chat server

# Starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

# Broadcast message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle client connection
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            # Remove and close client if there is an error
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} has left the chat.'.encode('utf-8'))
            usernames.remove(username)
            break

# Receive new clients
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('USERNAME'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client)

        print(f"Username of the client is {username}")
        broadcast(f"{username} has joined the chat!".encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        # Start handling thread for each client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print(f"Server is listening on {HOST}:{PORT}...")
receive()
