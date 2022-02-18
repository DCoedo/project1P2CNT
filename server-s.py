import socket
import signal
import sys
import argparse

def readMsg(client, target):
    connected = True
    client.settimeout(10)
    msg = b""
    bytes_read = 0
    while connected:
        try:
            msg = client.recv(1024)
        except Exception:
            sys.stderr.write("ERROR:")
            connected = False
        if msg == target:
            connected = False
        bytes_read += len(msg)
    return bytes_read

def handle_client():
    PORT = int(sys.argv[1])
    IP = '0.0.0.0'
    ADDR = (IP, PORT)
    FORMAT = 'utf-8'

    connected = True
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)

    try:
        server.bind(ADDR)
    except Exception:
        sys.stderr.write("ERROR:")
        exit(1)

    server.settimeout(10)
    server.listen(10)

    while connected:
        try:
            connection, connection_address = server.accept()
            connection.send(bytes('accio\r\n', FORMAT))
            confirm_1_bytes = readMsg(connection, b'confirm-accio\r\n')
            connection.send(bytes('accio\r\n', FORMAT))
            confirm_2_bytes = readMsg(connection, b'confirm-accio-again\r\n\r\n')
            total_bytes = readMsg(connection, b"")
            total_bytes = total_bytes - confirm_1_bytes + confirm_2_bytes
            connection.close()
            print(total_bytes)
        except Exception:
            sys.stderr.write("ERROR")
            exit(2)

handle_client()
