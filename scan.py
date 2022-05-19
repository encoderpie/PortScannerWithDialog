#! /usr/bin/env python3

import sys, locale, socket
from timeit import default_timer as timer
from datetime import datetime
from dialog import Dialog

locale.setlocale(locale.LC_ALL, '')

d = Dialog(dialog='dialog')
d.set_background_title('Port Scanner With pythondialog - Encoderpie')
d.add_persistent_args(['--no-nl-expand'])

# Help menu def
def helpMenu():
    d.msgbox('''
After entering the IP or Host name and pressing the "OK" button, \
the "Port scanning operations" menu will appear on your screen. \
After selecting the option that suits you in this menu, \
you will be prompted to enter a port, after entering the port, \
the port scanning process will begin.
''', width=0, height=0, title='Help')

# Default ports
defaultStartPort = 1
defaultEndPort = 65534

# Port scan
def portScan(targetInput, startPort, endPort):
    try:
        target = socket.gethostbyname(targetInput)
        scanningPortsText = f'Scanning port(s): {startPort} - {endPort}'
        if (startPort == endPort):
            scanningPortsText = f'Scanning port: {startPort}'
        try:
            gauge_text = f'''
Scanning target: {target} 
Scanning started at: {str(datetime.now())}
{scanningPortsText}
Open port(s):
            '''
            d.gauge_start(text=gauge_text, height=0, width=0, percent=0, title='Port(s) Scanning...')
            openPorts = []
            startScanTime = timer()
            for port in range(startPort, endPort + 1):
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
            if (len(openPorts) == 0):
                openPortsText = f'{openPortsText}\n   The open port was not found.'
            for openport in openPorts:
                openPortsText = f'{openPortsText}\n   {str(openport)} is open port'
            startEndTimeDiffText = int(startfinishDiffTime)
            if (startEndTimeDiffText > 0):
                openPortsText = f'{openPortsText}\nPort scan process took {str(startEndTimeDiffText)} seconds'
            msg = f'Port scanning completed!\nOpen port(s): {openPortsText}'
        except KeyboardInterrupt:
            msg = 'Goodbye.'
        except socket.gaierror:
            msg = 'Hostname Could Not Be Resolved.'
        except socket.error:
            msg = 'Server not responding.'
    except:
        msg = 'Please enter a valid IP or Host address.'
    d.msgbox(f'{msg}\nExiting!', width=0, height=0, title='Result')  
    sys.exit(0)

# PORT input menu 
def portInputScreen(ip):
    userPortFormat = d.menu(f'Target IP/Hostname: {str(ip)}\nSelect the port scanning process.',
                            choices=[
                                ('1.', f'Scan all ports between {defaultStartPort} and {defaultEndPort}'), 
                                ('2.', 'Scan a single port'), 
                                ('3.', 'Scan all ports in the specified range')],
                            height=None, width=None, menu_height=None, title='Port scanning process')[1]
    if (userPortFormat == '1.'):
        portScan(ip, defaultStartPort, defaultEndPort)
    elif (userPortFormat == '2.'):
        code, userPortSingle = d.inputbox('Input port', init='80', width=0, height=0, title='Port', help_button=True)
        if code == d.OK:
            portScan(ip, int(userPortSingle), int(userPortSingle))
    elif (userPortFormat == '3.'):
        code, userPortRange = d.inputbox('Input port range', init='80 443', width=0, height=0, title='Port range', help_button=True)
        if code == d.OK:
            portRangeParsed = userPortRange.split(' ')
            portScan(ip, int(portRangeParsed[0]), int(portRangeParsed[1]) - 1)
    if code == d.CANCEL:
        msg = 'You pressed the Cancel button in the previous menu.'
    elif code == d.ESC:
        msg = 'You pressed the Escape key in the previous menu.'
    elif code == d.HELP:
        helpMenu()
    d.msgbox(f'{msg}\nExiting!', width=0, height=0, title='Exiting')
    sys.exit(0)

# IP input menu
def ipInputScreen():
    code, target = d.inputbox('Input target IP or Host address', init='192.168.', width=0, height=0, title='IP or Host name', help_button=True)
    if code == d.OK:
        portInputScreen(target)
    elif code == d.CANCEL:
        msg = 'You pressed the Cancel button in the previous menu.'
    elif code == d.ESC:
        msg = 'You pressed the Escape key in the previous menu.'
    elif code == d.HELP:
        helpMenu()
    d.msgbox(f'{msg}\nExiting!', width=0, height=0, title='Exiting')
    sys.exit(0)

# Welcome screen
welcomeScreen = d.msgbox('''
Welcome to Port Scanner With pythondialog, \
Press the 'OK' button at the bottom to start scanning the IP, \
press the 'help' button at the bottom to get help.
''', width=0, height=0, title='Port Scanner With pythondialog', help_button=True)
if welcomeScreen == d.OK:
    ipInputScreen()
elif welcomeScreen == d.HELP:
    helpMenu()
sys.exit(0)