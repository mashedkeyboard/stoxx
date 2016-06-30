#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3

# Define functions

# Sets up database
def dbSetup():
    # Database connection
    global c
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS stock (ID INTEGER PRIMARY KEY, Name str, Price float, numStock int);")

# Counts letters
def cletters(word):
    return len(word) - word.count(' ')

# Lists stock for use
def listStock():
        # Database connection
        global c
        conn = sqlite3.connect('stock.db')
        c = conn.cursor()
        c.execute("SELECT * FROM stock")
        rows = c.fetchall()
        return(str(rows))

# Searches stock in database
def srcStock(sockconn):
    # Database connection
    global c
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    try:
        itemsToReturn = []
        sendstr = "CMD ACC SEND STKNM"
        sockconn.send(bytes(sendstr, 'UTF-8'))
        data = sockconn.recv(512).decode("utf-8")
        c.execute('SELECT * FROM stock WHERE Name LIKE "%' + data + '%";')
        while True:
            row = c.fetchone()
            if not row:
                break
            else:
                itemsToReturn.append([str(row[0]),str(row[1]),str(row[2]),str(row[3])])
            sockconn.send(bytes(str(itemsToReturn), 'UTF-8'))
            
    except ValueError:
        sendstr = "INPUT ERR"
        sockconn.send(bytes(sendstr, 'UTF-8'))
        return(False)

# Adds stock to database
def addStock(sockconn):
    try:
        stg = 1
        while 1:
            if (stg == 1):
                sendstr = "CMD ACC SEND STKNM"
            elif (stg == 2):
                stkname = data
                sendstr = "SEND STKCOUNT"
            elif (stg == 3):
                stkcount = data
                sendstr = "SEND STKPRICE"
            elif (stg == 4):
                stkprice = data
                sendstr = "CONF ADD STKNM=" + stkname + ",STKCOUNT=" + stkcount + ",STKPRICE=" + stkprice + ",STKNAME=" + stkname
            elif (stg == 5):
                if data == "Y" or data == "y":
                    break
                else:
                    return(False)
            stg += 1
            sockconn.send(bytes(sendstr, 'UTF-8'))
            data = sockconn.recv(512).decode("utf-8")

        try:
            # Database connection
            global c
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute('INSERT INTO stock (Name, Price, numStock) VALUES ("' + stkname + '", ' + str(stkprice) + ', ' + str(stkcount) + ');')
            conn.commit()
            c.execute('SELECT ID FROM stock WHERE ID="' + str(c.lastrowid) + '";')
            return(str(c.fetchone()[0]))
        except Exception as e:
            sendstr = "ADD ERR"
            sockconn.send(bytes(sendstr, 'UTF-8'))
            return(False)
        else:
            sendstr = "ADD ERR"
            sockconn.send(bytes(sendstr, 'UTF-8'))
            return(False)
        
    except ValueError:
        sendstr = "INPUT ERR"
        sockconn.send(bytes(sendstr, 'UTF-8'))
        return(False)

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
