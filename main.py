import re #regular expressions
import sqlite3 #https://docs.python.org/3/library/sqlite3.html


#variable declaration
materialInput = '' #user input
materialOutput = '' #successor material output
matchFound = False #set to true when match is found
swChangesRequired = False #true if software changes are required
directSuccessor = False #true if there is a direct successor found
nonDirectMsg = '' #message shown when there is no direct successor
workerStr = '' #used for string manipulation operations
runAgainBool = True
runAgainInput = ''
validRunAgainInput = False #True if Y/y/N/n is entered when asked if customer would like to enter another material number

#----- Regex Cheat Sheet -----#
# "^": Start of line/string
# "\.": escape input to use "."
# ".": matches any character (except for line terminators)
# "+": matches the previous token between one and unlimited times

while runAgainBool == True:
    #----- Get User Input -----#
    materialInput = input("Please enter the material number of the obsolete part\n") #user input
    materialInput = str(materialInput).upper() #convert input to uppercase
    materialInput = materialInput.strip() #remove whitespace from front and back
    print("Finding successor product for %s...\n" % (materialInput)); #formatted string

    #----- Products that don't use database lookup first -----#


    ### Inverters ###
    # P64 S2
    matchResult = re.match(r"^8I64S2.+\.00X-1$", materialInput) #match if string matches format 8I64S2*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        workerStr = strPartition[0].removeprefix("8I64S2") #eliminate the prefix so we can use isolate the rest of the model number
        materialOutput = "8I64S2%s.0X-000" % (workerStr) #generate the successor model number
        swChangesRequired = False #software changes not needed
        directSuccessor = True

    # P64 T2
    matchResult = re.match(r"^8I64T2.+\.00X-1$", materialInput) #match if string matches format 8I64T2*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        #strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        #workerStr = strPartition[0].removeprefix("8I64T2") #eliminate the prefix so we can use isolate the rest of the model number
        #materialOutput = "8I66T2%s.0X-000" % (workerStr) #generate the successor model number (P66)
        
        swChangesRequired = True #software changes not needed
        directSuccessor = False
        nonDirectMsg = "Transition to P66."

    # P64 T4
    matchResult = re.match(r"^8I64T4.+\.00X-1$", materialInput) #match if string starts with 8I64T4*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        workerStr = strPartition[0].removeprefix("8I64T4") #eliminate the prefix so we can use isolate the rest of the model number
        materialOutput = "8I64T4%s.0X-000" % (workerStr) #generate the successor model number
        swChangesRequired = False #software changes not needed
        directSuccessor = True

    # P74 S2
    matchResult = re.match(r"^8I74S2.+\.01P-1$", materialInput) #match if string matches format 8I74S2*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        workerStr = strPartition[0].removeprefix("8I74S2") #eliminate the prefix so we can use isolate the rest of the model number
        materialOutput = "8I74S2%s.0P-000" % (workerStr) #generate the successor model number
        swChangesRequired = False #software changes not needed
        directSuccessor = True


    # P74 T4
    matchResult = re.match(r"^8I74T4.+\.01P-1$", materialInput) #match if string matches format 8I74T4*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        workerStr = strPartition[0].removeprefix("8I74S2") #eliminate the prefix so we can use isolate the rest of the model number
        materialOutput = "8I74T4%s.0P-000" % (workerStr) #generate the successor model number
        swChangesRequired = False #software changes not needed
        directSuccessor = True

    # P84 T2
    matchResult = re.match(r"^8I84T2.+\.01P-1$", materialInput) #match if string matches format 8I64T2*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        #strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        #workerStr = strPartition[0].removeprefix("8I64T2") #eliminate the prefix so we can use isolate the rest of the model number
        #materialOutput = "8I66T2%s.0X-000" % (workerStr) #generate the successor model number (P66)
        
        swChangesRequired = True #software changes not needed
        directSuccessor = False
        nonDirectMsg = "Transition to P66."

    # P84 T4
    matchResult = re.match(r"^8I84T4.+\.01P-1$", materialInput) #match if string matches format 8I64T2*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        #strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        #workerStr = strPartition[0].removeprefix("8I64T2") #eliminate the prefix so we can use isolate the rest of the model number
        #materialOutput = "8I66T2%s.0X-000" % (workerStr) #generate the successor model number (P66)
        
        swChangesRequired = True #software changes not needed
        directSuccessor = False
        nonDirectMsg = "Transition to P66 or P86 depending on performance needed."



    ### Safety PLCs ###
    # X20SL80xx
    matchResult = re.match(r"^X20SL80.{2}$", materialInput) #match if matches format X20SL80xx
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        strPartition =  materialInput.partition("80") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        workerStr = strPartition[0].removeprefix("8I64S2") #eliminate the prefix so we can use isolate the rest of the model number
        materialOutput = "X20SL81%s" % (strPartition[2]) #generate the successor P64new model number
        swChangesRequired = True #software changes not needed


    ### Motors ###


    ### 


    #----- Wrap Up and Output -----#
    if matchFound == True: #If a regex match was found
        if directSuccessor == True: #if successor was found
            print("The replacement material number is %s\n" % (materialOutput)) #print output
        else:
            print("No direct successor. %s\n" % (nonDirectMsg)) 

        if swChangesRequired == True: #if software changes are required
            print("Software changes will be necessary in Automation Studio.\n")
        else: 
            print("No software changes required.\n")

    else:
        #In cases that a successor could not be found there either is not a successor or there was a typo in the input
        print("Unfortunately, there is no successor product for the entered material number. Please ensure there are no mistakes in your input.\n ") 
    
    #----- Go Again? -----#
    validRunAgainInput = False
    while validRunAgainInput == False:
        runAgainInput = input("Would you like to enter another material number? (y/n)\n")
        if runAgainInput == 'Y' or runAgainInput == 'y':
            validRunAgainInput = True
            runAgainBool = True
        elif runAgainInput == 'N' or runAgainInput == 'n':
            validRunAgainInput = True
            runAgainBool = False
        else:
            validRunAgainInput = False
            print("Please enter a valid input (y/n).")



