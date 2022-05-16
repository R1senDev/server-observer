import os
import time
from colorama import init
init()
from colorama import Fore, Back, Style
print(Fore.WHITE)
os.system('clear')

try:
    flist = open('list.txt')
except FileNotFoundError:
    flist = open('list.txt', 'x')
    flist = open('list.txt')
servers = flist.readline().split(' ')
flist.close()

if servers == ['']:
    print('Enter the adresses of the monitored servers, separating them with a space:')
    rawservers = input()
    servers = rawservers.split(' ')
    y = input('\nSave this list of servers? [Y/N] ')
    if (y.lower() == 'y'):
        flist = open('list.txt', 'w')
        flist.write(rawservers)
        flist.close()

response = 0
sent = 0
ok = 0
lost = 0

try:
    while True:
        try:
            os.system('clear')
            for addr in servers:
                starttime = time.time()
                response = os.system('ping -c 1 ' + addr + ' &> /dev/null')
                timedelta = time.time() - starttime
                sent += 1
                if response == 0:
                    print(Fore.WHITE + addr + ': ' + Fore.GREEN + 'OK')
                    ok += 1
                else:
                    print(Fore.WHITE + addr + ': ' + Fore.RED + 'lost' + Fore.WHITE + ' (code ' + str(response) + ')')
                    lost += 1
                if timedelta >= 0.50:
                    pingfore = Fore.RED
                elif timedelta >= 0.20:
                    pingfore = Fore.YELLOW
                else:
                    pingfore = Fore.GREEN
                print(pingfore + '(Ping: ' + str(int(timedelta * 100000) / 100) + ' msec)')
                print()
            print(Fore.WHITE + '=== STATISTICS ===')
            print('    Total packets sent: ' + str(sent))
            print('        "OK" responses: ' + str(ok))
            print('        Lost responces: ' + str(lost))
            try:
                if lost / sent >= 0.25:
                    print(Fore.RED + ' Packet lost frequency: ' + str(int(lost / sent * 100)) + '%')
                elif lost / sent >= 0.1:
                    print(Fore.YELLOW + ' Packet lost frequency: ' + str(int(lost / sent * 100)) + '%')
                elif (ok == 0) and (lost > 0):
                    print(Fore.RED + ' Packet lost frequency: 100%')
                else:
                    print(Fore.GREEN + ' Packet lost frequency: ' + str(int(lost / sent * 100)) + '%')
            except:
                print(Fore.GREEN + ' Packet lost frequency: 0%')
            print(Fore.WHITE + '\nPress [Ctrl]+[C] to pause')
            time.sleep(1)
        except KeyboardInterrupt:
            os.system('clear')
            print(Fore.YELLOW + '             === PAUSED ===\n\n' + Fore.WHITE + '        Press [Enter] to continue\nPress [R]->[Enter] to reset servers list\n    Press [Ctrl]+[C]->[Enter] to exit' + Fore.BLACK)
            y = input()
            if y.lower() == 'r':
                os.system('rm list.txt')
                os.system('python start.py')
                exit
except KeyboardInterrupt:
    os.system('clear')

