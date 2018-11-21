import roPY
import requests
import time
import ctypes
import sys

ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
ctypes.windll.kernel32.SetConsoleTitleW(f'Cookie checker | Lines left: 0 | Total Robux: 0 | After tax: 0')

i = open('input.txt', 'r').read().splitlines()
o = open('output.txt', 'w')
var = 0
lineVar = len(i)

def sex():
    for combo in i:
        global var
        global lineVar
        global Format
        robuxValue = roPY.getRobux(combo)
        user = roPY.getUsernameFromCookie(combo)
        if robuxValue == '0':
            print('\x1b[0;31;40m' + combo + '\x1b[0m' + '\n' + robuxValue + '\n' + '\n' + '\n')
            pass
        elif robuxValue != '0':
            print('\x1b[0;32;40m' + combo + '\x1b[0m' + '\n' + user + ':' + robuxValue + '\n' + '\n' + '\n')
            pass

        #variables
        user=user
        robux=robuxValue
        cookie=combo

        o.write(f'{robux}:{user}:{cookie}' + '\n')
        #variables for console titles
        lineVar = lineVar - 1
        var = int(robuxValue) + var
        afterTax = int(round(var - var / 100 * 30 ))
        ctypes.windll.kernel32.SetConsoleTitleW(f'Cookie checker | Lines left: {lineVar} | Total Robux: {var} | After tax: {afterTax} ')
        if lineVar == 0:
            break
sex()

print(f'Total Robux: {var}')
o.write(f'Total Robux: {var}')
o.close()
input('Press enter to close!')
