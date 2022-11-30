import socket
import threading

import email
from io import StringIO
import hashlib
import base64;  

#https://docs.python.org/3/howto/sockets.html

HEADER = 64 #may need to change this value to adjust for video streaming flow or like websockets    
HANDSHAKE = ''
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
#be aware of bug which can occur if PORT 5050 is in use

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
#socker.socket()is a function which defines the socket
#.bind() is a method which tells the socket which machine is the source of the connection and which port it will be broadcasting from

#First param indicates what addresses our socket can communicate with
#Second param defines how information will be passed to the socket
#In this example we set up an IPV4 connection where data will be constantly streamed

## write a test suite for this using MDN Docs example:
# So if the Key was "dGhlIHNhbXBsZSBub25jZQ==", the Sec-WebSocket-Accept header's value is "s3pPLMBiTxaQ9kYGzzhZRbK+xOo="
## very useful documentation => https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers
## also very useful https://sookocheff.com/post/networking/how-do-websockets-work/
def websocket_handshake(client_msg):

    _, client_msg = client_msg.split('\r\n', 1)
    message = email.message_from_file(StringIO(client_msg))
    headers = dict(message.items())
    m = hashlib.sha1()
    
    # print(headers["Sec-WebSocket-Key"])

    m.update((headers['Sec-WebSocket-Key'] +  "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode('utf-8'))
    m = base64.b64encode(m.digest())
    myHand = f'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: {m}'


    return myHand.encode('UTF-8')

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} is connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        print(msg_length)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False

            print(f"[{addr} {msg}]")

    conn.close()

        # each packet of information contains a header which defines the size of the packet
        # here we are telling the server to only accept messages that are size HEADER defined as 64 bytes.
        # we also need to decode the message from bytecode (01010101) because messages through the wire are encoded in that way
        # we will be encoding incoming messages from the client side in 'utf-8'
        # 'utf-8' is a string formate so we need to convert that back into an int
        # we can then recieve the proper message by listening for a msg that is the length that the HEADER proscribed
        # this is also a blocking line of code essentially it waits until the conn object recieves a packet from the client

def handle_webpack_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} is connected.")
    connected = True
    i = 1

    while connected:
        try:
            print("message no.", i)
            client_msg = conn.recv(1024).decode(FORMAT)
            my_hand = websocket_handshake(client_msg)
            conn.sendall(my_hand)
            i+=1
        except(KeyboardInterrupt, OSError):
            print("no it didn't work jackass")
            break
            connected = False
            conn.close()
        # connected = False
        # if handshake:
        #     # print(handshake)
        #     # connected = False

        #     msg = conn.recv(handshake).decode(FORMAT)
        #     if msg == DISCONNECT_MSG:
        #         connected = False

        #     print(f"[{addr} {msg}]")

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    #server is now listening for connections to 197.000.1:5050
    while True:
        conn, addr = server.accept()
        #server.accept() is a blocking operation so we won't accept new connections until 
        #conn returns a socket object which provides methods to communicate with the client
        #addr refers to the client's IPV4
        #we'll now pass each new connection to a handle_client thread which will deal with each connection individually (unnecessary for the purposes of this application)
        thread = threading.Thread(target=handle_webpack_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()