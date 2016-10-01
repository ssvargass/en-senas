import io
import socket
import struct
import time
import picamera

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.0.12', 8080))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')

