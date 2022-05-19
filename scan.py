#! /usr/bin/env python3

import sys, locale, socket
from timeit import default_timer as timer
from datetime import datetime
from dialog import Dialog

locale.setlocale(locale.LC_ALL, '')

d = Dialog(dialog='dialog')
d.set_background_title('Port Scanner With pythondialog - Encoderpie')
d.add_persistent_args(['--no-nl-expand'])

# Port scan def
def portScan():
    startPort = 1
    endPort = 65535
    try:
        target = socket.gethostbyname(user_input)
        try:
            gauge_text = '''
Scanning Target: {} \

Scanning started at: {}
Open ports:
            '''.format(target, str(datetime.now()))
            d.gauge_start(text=gauge_text, height=0, width=0, percent=0, title='Ports Scanning...')
            openPorts = []
            startScanTime = timer()
            for port in range(startPort, endPort):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                result = s.connect_ex((target,port))
                if result == 0:
                    openPorts.append(port)
                    gauge_text = f'{gauge_text} {str(port)}'
                    d.gauge_update(int((port/endPort)*100), text=gauge_text, update_text=True)
                s.close()
            startfinishDiffTime = timer() - startScanTime
            d.gauge_update(100)
            d.gauge_stop()
            openPortsText = ''
            for openport in openPorts:
                openPortsText = f'{openPortsText}\n   {str(openport)} is open port'
            openPortsText = f'{openPortsText}\nPort scan process took {str(int(startfinishDiffTime))} seconds'
            msg = f'Open ports: {openPortsText}'
        except KeyboardInterrupt:
            msg = 'Exiting Program.'
        except socket.gaierror:
            msg = 'Hostname Could Not Be Resolved.'
        except socket.error:
            msg = 'Server not responding.'
    except:
        msg = 'Please enter a valid IP or Host address.'
    d.msgbox(f'{msg}\nExiting!', width=0, height=0, title='Result')  
    sys.exit(0)

# Help menu def
def helpMenu():
    d.msgbox(''' \

Welcome to Port Scanner With pythondialog, \
Press the 'OK' button at the bottom to start scanning the IP, \
press the 'help' button at the bottom to get help.
''', width=0, height=0, title='Help')

# Welcome screen
welcomeScreen = d.msgbox(''' \

Welcome to Port Scanner With pythondialog, \
Press the 'OK' button at the bottom to start scanning the IP, \
press the 'help' button at the bottom to get help.
''', width=0, height=0, title='Port Scanner With pythondialog', help_button=True)

if welcomeScreen == d.HELP:
    helpMenu()

# IP, PORT input
code, user_input = d.inputbox('Input target IP or Host address', init='192.168.', width=0, height=0, title='IP or Host name', help_button=True)

if code == d.OK:
    portScan()
elif code == d.CANCEL:
    msg = 'You chose the Cancel button in the previous dialog.'
elif code == d.ESC:
    msg = 'You pressed the Escape key in the previous dialog.'
elif code == d.HELP:
    helpMenu()
else:
    msg = 'Unexpected exit code from d.inputbox(). Please report a bug.'

d.msgbox(f'{msg}\nExiting!', width=0, height=0, title='Exiting')  

sys.exit(0)