import datetime
import io

import colorama
from colorama import Fore

colorama.init()


def log_err(a):
    today = datetime.datetime.today()
    t = "[" + today.strftime("%H:%M:%S - %d.%m.%y") + "] " + a
    err = io.open('logs/err.txt', "a", encoding="utf-8")
    err.write(t + '\n')
    err.close()
    inf = io.open("logs/inf.txt", "a", encoding="utf-8")
    inf.write(t + '\n')
    inf.close()
    deb = io.open("logs/deb.txt", "a", encoding="utf-8")
    deb.write(t + '\n')
    deb.close()
    print(Fore.RED + "[" + today.strftime("%H:%M:%S - %d.%m.%y") + "] " + Fore.WHITE + a)


def log_inf(a):
    today = datetime.datetime.today()
    t = "[" + today.strftime("%H:%M:%S - %d.%m.%y") + "] " + a
    inf = io.open("logs/inf.txt", "a", encoding="utf-8")
    inf.write(t + '\n')
    inf.close()
    deb = io.open("logs/deb.txt", "a", encoding="utf-8")
    deb.write(t + '\n')
    deb.close()
    print(Fore.YELLOW + "[" + today.strftime("%H:%M:%S - %d.%m.%y") + "] " + Fore.WHITE + a)


def log_deb(a):
    today = datetime.datetime.today()
    t = "[" + today.strftime("%H:%M:%S - %d.%m.%y") + "] " + a
    deb = io.open("logs/deb.txt", "a", encoding="utf-8")
    deb.write(t + '\n')
    deb.close()
    print(Fore.GREEN + "[" + today.strftime("%H:%M:%S - %d.%m.%y") + "] " + Fore.WHITE + a)
