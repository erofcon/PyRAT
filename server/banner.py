from rich import print

ABOUT_BANNER = """
\t\t [bold red]PyRat[/bold red]
\t created by @erofcon
\t https://github.com/erofcon
"""

MAIN_BANNER = """

[bold yellow]Commands:[/bold yellow]

   help | h     \t show help 
   list | ls    \t get all connected client
   connect <ID> \t connect to client by <ID>

"""

CLIENT_BANNER = """

[bold yellow]Commands:[/bold yellow]

 help | h             \t  show help
 exit                 \t  exit to main menu
 geolocate            \t  get client geolocation with IP-address
 shell                \t  run shell
 download <filename>  \t  download file
 upload               \t  upload file

"""


def print_banner(banner_type: int):
    if banner_type == 0:
        print(MAIN_BANNER)

    elif banner_type == 1:
        print(CLIENT_BANNER)

    else:
        print('')
