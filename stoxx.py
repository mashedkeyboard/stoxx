#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

while True:
    while True:
        try:
            selector = int(input("Press 1 for Stoxx Warehousing. Press 2 for StoxxUtils . Press 3 for Stoxx Server. Press 4 to quit. > "))
            break
        except ValueError:
            print("That's not an option.")
    if selector == 1:
        os.system("stock\stockmanager.py")
    elif selector == 2:
        os.system("chk\GTINcheck.py")
    elif selector == 3:
        os.system("stocksvc\stockserver.py")
    elif selector == 4:
        break
    else:
        print("That's not an option.")
