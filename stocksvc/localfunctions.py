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
            data = conn.recv(512).decode("utf-8")

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
        conn.send(bytes(sendstr, 'UTF-8'))
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
