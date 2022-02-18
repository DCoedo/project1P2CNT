import socket
import signal
import sys
import argparse


def readMsg(client, target, confirm):
    connected = True
    client.settimeout(10)
    msg = b""
    bytes_read = 0
    while connected:
        try:
            if confirm:
                msg += client.recv(8)
            else:
                msg = client.recv(8)
        except Exception:
            sys.stderr.write("ERROR")
            connected = False
        if msg == target:
            connected = False
        if not confirm:
            bytes_read += len(msg)
    if confirm:
        bytes_read += len(msg)
    return bytes_read

def handle_client():
    PORT = int(sys.argv[1])
    IP = '0.0.0.0'
    ADDR = (IP, PORT)

    connected = True
    FORMAT = 'utf-8'
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
        
        signal.signal(signal.SIGINT, exit)
        connection, connection_address = server.accept()
        connection.send(bytes('accio\r\n', FORMAT))
        confirm_1_bytes = readMsg(connection, b'confirm-accio\r\n', True)
        print(confirm_1_bytes)
        connection.send(bytes('accio\r\n', FORMAT))
        confirm_2_bytes = readMsg(connection, b'confirm-accio-again\r\n\r\n', True)
        print(confirm_2_bytes)
        all_bytes = readMsg(connection, b"", False) - confirm_1_bytes + confirm_2_bytes
        connection.close()
        print(all_bytes)


handle_client()
