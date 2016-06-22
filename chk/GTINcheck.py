## GTIN-8 calculator
## Copyright (c) MashedKeyboard 2016
## All rights reserved

## Begin import libraries
import math
## End libraries

## Begin globals
global GTIN
GTIN = int(0)
## End globals

## Begin function definitions
def gtinCheck():
    global GTIN
    inputgtin = int(input("Enter a 7-digit GTIN without a check digit > "))
    if (len(str(abs(inputgtin))) != 7):
        print("Please enter a 7-digit GTIN without a check digit")
        gtinCheck()
    GTIN = inputgtin
    return inputgtin
def isEven(number):
        return number % 2 == 0
def isMultOf10(number):
        return number % 10 == 0
def roundup(x):
        return int(math.ceil(x / 10)) * 10
## End function definitions

## Begin program
print("Welcome to StoxxUtils GTIN-8 Calculation")
while True:
    print("")
    iterator = 0
    numsGen = list()
    for chkDig in str(gtinCheck()):
        intChk = int(chkDig)
        if (isEven(iterator)):
            numsGen.append(intChk * 3)
        else:
            numsGen.append(intChk * 1)
        iterator = iterator + 1
    sumNumsGen = sum(numsGen)
    if (isMultOf10(sumNumsGen)):
        numsGen.append(0)
        print("Invalid GTIN.")
    else:
        gtinChkDig = str(roundup(sumNumsGen) - sumNumsGen)
        print("Valid GTIN. Check digit is " + str(gtinChkDig))
        print("Full GTIN code is " + str(GTIN) + str(gtinChkDig))
    input("Press Enter to check another code or Ctrl-C to exit")


