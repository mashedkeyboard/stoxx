# Stock management system
# Curtis Parfitt-Ford (c) 2016

# Import libraries
import os.path
import configparser
import localfunctions
import networkfunctions

# Config parser
global Config
Config = configparser.ConfigParser()
Config.read("stoxx.ini")

# Initialization
try:
    Config.get("LICENSE", "LicenseNo")
except:
    input("Error getting license details. Check your license and try again. Press any key to quit.")
    quit()

# One time setup
if Config.get("SETTINGS", "FirstRun") == "1":
    print("---")
    print("Thank you for purchasing the StoXX Stock Management System!")
    print("---")
    nlocal = input("Do you need to use a networked database? (y/[n])")
    if nlocal == "y":
        Config.set("SETTINGS", "isnetworked", "1")
        networkfunctions.networkSetup()
    else:
        localfunctions.dbSetup()
        Config.set("SETTINGS", "isnetworked", "0")
    Config.set("SETTINGS", "FirstRun", "0")
    cfgfile = open("stoxx.ini",'w')
    Config.write(cfgfile)
    cfgfile.close()
    print("Thanks, setup complete! Wasn't that easy :)")

# Program mainloop starts
print("")
print("Welcome to StoXX Stock Management System")
print("")
if (Config.get("SETTINGS", "isnetworked") == "1"):
    networkfunctions.networkConnect()
while True:
    while True:
        try:
            while True:
                try:
                    print("")
                    print("Press 1 for a stock list. Press 2 to add a stock item. Press 3 to restock. Press 4 to run a stock query. Press 5 to delete a stock item. Press 6 for help.")
                    print("")
                    menuOption = int(input("> "))
                    break
                except ValueError:
                        print("That wasn't a valid option. Try again.")
            # Listing stock
            if menuOption == 1:
                localfunctions.listStock()
                break
            # Grabbing stock information for adding to db
            elif menuOption == 2:
                n = input("Enter the stock item name > ")
                doneprice = False
                donestock = False
                while doneprice == False:
                    try:
                       price = float(input("Enter the price of the item > "))
                       doneprice = True
                    except ValueError:
                        print("That wasn't a valid price. Try again.")
                while donestock == False:
                    try:
                        stockNum = int(input("Enter the number of the item in stock > "))
                        donestock = True
                    except ValueError:
                        print("That wasn't a valid stock number. Try again.")
                # Call to add stock function
                localfunctions.addStock(n, price, stockNum)
                break
            # Restocking code
            elif menuOption == 3:
                while True:
                    searchselector = input("Press 1 to search by stock ID. Press 2 to search by stock name.")
                    if searchselector == '1':
                        stockid = input("Enter the stock ID you wish to add stock to > ")
                        if localfunctions.stockFillById(stockid) == True:
                            break
                    elif searchselector == '2':
                        stockname = input("Enter the stock name you wish to add stock to > ")
                        if localfunctions.stockFillByName(stockname) == True:
                            break
                    else:
                        print("Invalid input. Try again.")
                break
            elif menuOption == 4:
                localfunctions.findStock()
                break
            elif menuOption == 5:
                localfunctions.deleteStock()
                break
            elif menuOption == 6:
                print("Please consult the user documentation, available at stoxx.mashedkeyboard.me, for help. If there's some other issue, please feel free to contact curtis@mashedkeyboard.me.")
                print(" --- ")
                print(" Stoxx 2016 ")
                print(" Licensed to: " + Config.get("LICENSE", "LicenseeName"))
                print(" Licensee company: " + Config.get("LICENSE", "LicenseeCompany"))
                print(" License number: " + Config.get("LICENSE", "LicenseNo"))
                print(" --- ")
                break
            else:
                print("Invalid option. Try again.")
                break
        except ZeroDivisionError as e:
            print("---")
            print("Hmm, the program tried to divide by zero. That was odd. Contact curtis@mashedkeyboard.me with the following error:" + str(e))
            print("---")
            input("Press Enter to try and continue the program, or Control-C to quit.")
            break
        except KeyboardInterrupt as e:
            while True:
                print("---")
                try:
                    print("Press 1 to quit, or press 2 to return to the main menu.")
                    print("---")
                    selectType = int(input("> "))
                except ValueError:
                    print("That wasn't a valid option. Try again.")
                if (selectType == 1 ):
                    quit()
                elif (selectType == 2):
                    break
                else:
                    print("That wasn't a valid option. Try again.")
        except Exception as e:
            print("---")
            print("Argh! You found an uncaught exception. That's never good! Contact curtis@mashedkeyboard.me with the following error:")
            print(str(e))
            print("---")
            input("Press Enter to try and continue the program, or Control-C to quit.")
            break
