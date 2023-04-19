import tkinter as tk
#import guiFun
from lookup import *

#----- VERSION -----#
sofwareVersion = '0.41b'

#----- Variable Declaration -----#
rawInput = None
materialInputList = list()
#materialInput = '' #user input
materialOutput = '' #successor material output
matchFound = False #set to true when match is found
swChangesRequired = False #true if software changes are required
anySuccessor = False
directSuccessor = False #true if there is a DIRECT or 1:1 successor found
nonDirectMsg = '' #message shown when there is no DIRECT or 1:1 successor
situationalMsg = ''
workerStr = '' #used for string manipulation operations
runAgainBool = True
runAgainInput = ''
validRunAgainInput = False #True if Y/y/N/n is entered when asked if customer would like to enter another material number
validInput = False #True if the input material was found in the database



print("***WELCOME TO THE B&R SUCCESSOR PRODUCT FINDER v%s***\nWritten by Chris Hairston" % sofwareVersion);



while runAgainBool == True: #core code is in while loop so user can do lookup as many times as desired
    #----- Get User Input -----#
    rawInput = input("Please enter the material number(s) of the obsolete parts (multiple parts can be seperated by commas) \n(PC configurations must be broken down into individual component materials)\n") #user input
    rawInput = str(rawInput).upper() #convert input to uppercase
    materialInputList = rawInput.split(",")
    for materialInput in materialInputList:

        lookupResult = getSuccessor(materialInput)
        
        materialOutput = lookupResult.materialOutput
        nonDirectMsg = lookupResult.nonDirectMsg
        situationalMsg = lookupResult.situationalMsg
        matchFound = lookupResult.matchFound
        directSuccessor = lookupResult.directSuccessor
        anySuccessor = lookupResult.anySuccessor
        validInput = lookupResult.validInput

        #----- Wrap Up and Output -----#
        if situationalMsg != '' and situationalMsg != None:
            print(situationalMsg) 
        elif anySuccessor == True: #If any successor is available
            if directSuccessor == True: #if direct successor was found
                print("The replacement material number(s) is (are):\n%s" % (materialOutput)) #print output
                
            else:
                print("No direct successor found. %s\n" % (nonDirectMsg))

            print("(Please ensure that this successor is not obsolete itself.)\n") #disclaimer

            if swChangesRequired == True: #if software changes are required
                print("Software changes will be necessary in Automation Studio.\n")
            else: 
                print("No software changes required.\n")
        else:
            if validInput:
                print("The input material appears to be valid. However, there unfortunately is no successor product.")
            else:    
                #In cases there was a typo in the input, the input is not obsolete, or the material is missing from the program
                print("Unfortunately, a successor product for the entered material number is not available. The entered material is either not obsolete, there are mistakes in your input or this program is missing this material.\n ") 


    print("To report an issue or missing material, create an issue at https://github.com/ChrisHairstonBnR/Python-Successor-Finder/issues\n")
  
    #----- Go Again? -----#
    validRunAgainInput = False
    while validRunAgainInput == False:
        runAgainInput = input("Would you like to enter another (more) material number(s)? (y/n)\n")
        if runAgainInput == 'Y' or runAgainInput == 'y':
            validRunAgainInput = True
            runAgainBool = True
        elif runAgainInput == 'N' or runAgainInput == 'n':
            validRunAgainInput = True
            runAgainBool = False
        else:
            validRunAgainInput = False
            print("Please enter a valid input (y/n). ")



