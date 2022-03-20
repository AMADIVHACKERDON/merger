import socket

HEADER = 97
PORT = 5050
DISCONNECTED_msg = '!DISCONNECT'
FORMAT = 'utf-8'
SERVER = "127.0.0.1"
ADDR = (socket.gethostname(),5050)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b'' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    print(message)

send('HELLOWORLD')