+#!/usr/bin/python
+# -*- coding: utf-8 -*-
import sqlite3

# Database connection
global c
conn = sqlite3.connect('stock.db')
c = conn.cursor()

# Define functions

# Sets up database
def dbSetup():
    c.execute("CREATE TABLE IF NOT EXISTS stock (ID INTEGER PRIMARY KEY, Name str, Price float, numStock int);")

# Counts letters
def cletters(word):
    return len(word) - word.count(' ')

# Lists stock for use
def listStock():
    c.execute("SELECT * FROM stock")
    row = c.fetchone()
    if not row:
        print("You have no stock added to the database.")
    else:
        print("---")
        print(" | ID | Name | Price | Stock |")
        while True:
            if row == None:
                break
            else:
                print(" | ",row[0], " | ", row[1], " | ", row[2], " | ", row[3]," | ")
                row = c.fetchone()
        print("---")

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
