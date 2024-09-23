import socket
import threading

# Choose a username
username = input("Enter your username: ")

# Client Information
HOST = '127.0.0.1'  # localhost
PORT = 12345        # Port number where server is running

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receiving messages from server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'USERNAME':
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred. Disconnecting from server.")
            client.close()
            break

# Sending messages to server
def send_messages():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('utf-8'))

# Start threads for receiving and sending messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
