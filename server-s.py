import socket
import sys
import argparse

IP = '0.0.0.0'
PORT = int(sys.argv[1])
ADDR = (IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDR)
except Exception:
    sys.stderr("ERROR")
    exit(1)

def readMsg(client, target):
    connected = True
    client.settimeout(10)
    msg = b""
    bytes_read = 0
    while connected:
        try:
            msg += connected.recv(2022)
        except Exception:
            sys.stderr.write("Error : CLIENT WAS TIMED OUT!")
            connected = False
        if msg == target:
            connected = False
        bytes_read += len(msg)
    return bytes_read

def handle_client():
    connected = True
    FORMAT = 'utf-8'
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while connected:
        connection, connection_address = server.accept()
        connection.send(bytes('accio\r\n', FORMAT))
        confirm_1_bytes = readMsg(connection, b'confirm-accio\r\n')
        connection.send(bytes('accio\r\n', FORMAT))
        confirm_2_bytes = readMsg(connection, b'confirm-accio-again\r\n\r\n')
        total_bytes = readMsg(connection, "")
        total_bytes = total_bytes - confirm_1_bytes + confirm_2_bytes
        connection.close()
        print(total_bytes)
