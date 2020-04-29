import time
import sys

bar = [
    " [=     ]",
    " [ =    ]",
    " [  =   ]",
    " [   =  ]",
    " [    = ]",
    " [     =]",
    " [    = ]",
    " [   =  ]",
    " [  =   ]",
    " [ =    ]",
]


def waiting():
    chars = "/—\|/—|"
    for char in chars:
        sys.stdout.write('\r' + 'Veuillez patienter... ' + char)
        time.sleep(.1)
        sys.stdout.flush()
