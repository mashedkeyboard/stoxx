+#!/usr/bin/python
+# -*- coding: utf-8 -*-
import sqlite3
import configparser
import socketsvc
import socket
import time

# Config parser
global Config
Config = configparser.ConfigParser()
Config.read("stoxx.ini")

# Define functions

# Sets up networking
def networkSetup():
    print("Please have your server details ready.")
    cfgfile = open("stoxx.ini",'w')
    serverip = input("Enter the server IP [127.0.0.1] > ")
    if serverip == "":
        serverip = "127.0.0.1"
    Config.set("NETWORKING", "serverip", serverip)
    serverport = input("Enter the server port [1785] > ")
    if serverport == "":
        serverport = "1785"
    Config.set("NETWORKING", "serverport", serverport)
    Config.write(cfgfile)
    cfgfile.close()

# Connects to networking server
def networkConnect():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((serverip, int(serverport)))
            break
        except:
            print("Error connecting to server. Retrying...")
            time.sleep(3)

# Make a request to the server
def networkRequest(request):
    try:
        while 1:
            data = client_socket.recv(512).decode("utf-8")
            if (data == 'q' or data == 'Q'):
                client_socket.close()
                break;
            else:
                print("RECIEVED:" , data)
                data = input ( "SEND( TYPE q or Q to Quit):" )
                if (data != 'Q' and data != 'q'):
                    client_socket.send(bytes(data, 'UTF-8'))
                else:
                    client_socket.send(bytes(data, 'UTF-8'))
                    client_socket.close()
                    break;
    except:
        print("Error connecting to server. Retrying...")
        time.sleep(3)

# Counts letters
def cletters(word):
    return len(word) - word.count(' ')

# Lists stock for use
def listStock():
    networkRequest(listStock)

# Adds stock to database
def addStock(stn, stockPrice, numinstock):
        c.execute('INSERT INTO stock (Name, Price, numStock) VALUES ("' + stn + '", ' + str(stockPrice) + ', ' + str(numinstock) + ');')
        conn.commit()
        print ("Stock added.")
        print("---")
        c.execute('SELECT ID FROM stock WHERE Name="' + stn + '";')
        print("The stock record ID is " + str(c.fetchone()[0]))
        print("---")

# Removes stock from database
def deleteStock():
    while True:
        try:
            idDelete = int(input("Enter the ID of the database item you want to delete > "))
            break
        except ValueError:
            print("That wasn't a valid ID. Try again.")
    c.execute('DELETE FROM stock WHERE ID="' + str(idDelete) + '";')
    conn.commit()
    print ("Stock deleted.")
    print("---")

# Restocks based on ID
def stockFillById(stid):
    c.execute('SELECT * FROM stock WHERE ID="' + stid + '";')
    strecrd = c.fetchone()
    print("---")
    print(str(strecrd))
    print("---")
    while True:
        itemRight = input("Is this the correct item? (y/n) > ")
        if itemRight == "n" or itemRight == "Y":
            return False
            break
        elif itemRight == "y" or itemRight == "Y":
            while True:
                try:
                    numStock = input("How much stock do you have right now? > ")
                    break
                except ValueError:
                    print("That wasn't a valid stock amount. Try again.")
            c.execute('UPDATE stock SET numStock = ' + numStock + ' WHERE id = ' + stid + ';')
            conn.commit()
            print("Complete.")
            print("---")
            return True
            break
        else:
            print("Invalid input, try again.")

# Restocks based on name
def stockFillByName(stnm):
    c.execute('SELECT * FROM stock WHERE Name="' + stnm + '";')
    strecrd = c.fetchone()
    print("---")
    print(str(strecrd))
    print("---")
    while True:
        itemRight = input("Is this the correct item? (y/n) > ")
        if itemRight == "n" or itemRight == "Y":
            return False
            break
        elif itemRight == "y" or itemRight == "Y":
            while True:
                try:
                    numStock = input("How much stock do you have right now? > ")
                    break
                except ValueError:
                    print("That wasn't a valid stock amount. Try again.")
            c.execute('UPDATE stock SET numStock = ' + numStock + ' WHERE id = ' + stnm + ';')
            conn.commit()
            print("Complete.")
            print("---")
            return True
            break
        else:
            print("Invalid input, try again.")

# finding stock
def findStock():
    while True:
        stockname = input("Enter the name of the stock you want to find > ")
        c.execute('SELECT * FROM stock WHERE Name = "' + stockname + '";')
        row = c.fetchone()
        if not row:
            print("You have no stock added to the database that matches that search.")
        else:
            print(str(len(row)) + " items in the database matching " + stockname)
            print("--- BEGIN RESULTS ---")
            print(" | ID | Name | Price | Stock |")
            while True:
                if row == None:
                    break
                else:
                    print(" | ",row[0], " | ", row[1], " | ", row[2], " | ", row[3]," | ")
                    row = c.fetchone()
            print("--- END RESULTS ---")
        input("Press Enter to continue > ")
        while True:
            try:
                gostay = int(input("Press 1 to search again, or 2 to go back to the main menu. > "))
                print("---")
            except ValueError:
                print("Oops, that wasn't a valid option. Try again.")
            if (gostay == 2):
                return
            elif (gostay != 1):
                print("Oops, that wasn't a valid option. Try again.")
