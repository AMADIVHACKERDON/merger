import socket as s
import threading

HEADER = 64
PORT = 5050
SERVER = s.gethostbyname(s.gethostname())
print(SERVER)
ADDR = (SERVER,PORT)
DISCONNECTED_msg = '!DISCONNECT'
FORMAT = 'utf-8'
server = s.socket(s.AF_INET,s.SOCK_STREAM)
server.bind(ADDR)

def HANDLE_CLIENT(conn,addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECTED_msg:
                connected = False

            print(f'[{addr}] {msg}')
            conn.send('Msg received'.encode(FORMAT))

    conn.close()



def start():
    server.listen()
    print(f'[LISTENING] server is listening on {SERVER}')

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=HANDLE_CLIENT, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print('[STARTING]server is starting...')
start()
