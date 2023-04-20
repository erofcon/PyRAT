ABOUT_BANNER = """
========== PyRat ==========
==== created by @erofcon =========
==== https://github.com/erofcon ==

"""

MAIN_BANNER = """

========== commands ==============

 help | h       ->  show help 
 list | ls      ->  get all connected client
 connect <ID>   ->  connect to client by <ID>



==================================
"""

CLIENT_BANNER = """

========== commands ==============

 help | h             ->  show help
 exit                 ->  exit to main menu
 geolocate            ->  get client geolocation with IP-address
 shell                ->  run shell
 download <filename>  ->  download file
 upload               ->  upload file

"""


def print_banner(banner_type: int):
    if banner_type == 0:
        print(MAIN_BANNER)

    elif banner_type == 1:
        print(CLIENT_BANNER)

    else:
        print('')
