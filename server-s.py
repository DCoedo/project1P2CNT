import socket
import signal
import sys
import argparse


def readConfirm(client, target):
    connected = True
    client.settimeout(10)
    msg = b""
    while connected:
        try:
            msg += client.recv(8)
        except socket.timeout:
            sys.stderr.write("ERROR:")
            break
        if msg == target:
            connected = False


def readMsg(client):
    connected = True
    client.settimeout(10)
    bytes_read = 0
    while connected:
        msg = b''
        try:
            msg = client.recv(8)
        except socket.timeout:
            sys.stderr.write("ERROR:")
            break
        if len(msg) == 0:
            break
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
    # print('Real bytes 1: ', len(b'confirm-accio\r\n'))
    # print('Real bytes 2: ', len(b'confirm-accio-again\r\n\r\n'))
    while connected:
        signal.signal(signal.SIGINT, exit)
        signal.signal(signal.SIGTERM, exit)
        connection, connection_address = server.accept()
        connection.send(bytes('accio\r\n', FORMAT))
        readConfirm(connection, b'confirm-accio\r\n')
        connection.send(bytes('accio\r\n', FORMAT))
        readConfirm(connection, b'confirm-accio-again\r\n\r\n')
        total_bytes = readMsg(connection)
        connection.close()
        print(total_bytes)


handle_client()
