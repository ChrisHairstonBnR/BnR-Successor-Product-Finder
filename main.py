import re #regular expressions
import sqlite3 #https://docs.python.org/3/library/sqlite3.html


#variable declaration
materialInput = '' #user input
materialOutput = '' #successor material output
matchFound = False #set to true when match is found
swChangesRequired = False #true if software changes are required
anySuccessor = False
directSuccessor = False #true if there is a DIRECT or 1:1 successor found
nonDirectMsg = '' #message shown when there is no DIRECT or 1:1 successor
workerStr = '' #used for string manipulation operations
runAgainBool = True
runAgainInput = ''
validRunAgainInput = False #True if Y/y/N/n is entered when asked if customer would like to enter another material number

#----- Regex Cheat Sheet -----#
# "^": Start of line/string
# "\.": escape input to use "."
# ".": matches any character (except for line terminators)
# "+": matches the previous token between one and unlimited times

#----- SQLite3 Setup -----#
dbConnection = sqlite3.connect("SuccessorProductDB.db")
dbCursor = dbConnection.cursor()
#dbConnection.row_factory = sqlite3.Row
dbResult = None #query result variable


while runAgainBool == True:
    #----- Get User Input -----#
    materialInput = input("Please enter the material number of the obsolete part\n") #user input
    materialInput = str(materialInput).upper() #convert input to uppercase
    materialInput = materialInput.strip() #remove whitespace from front and back
    print("Finding successor product for %s... " % (materialInput)); #formatted string
    print("(Please note that this program does not check if the material number entered is real.)\n") #disclaimer

    matchFound = False

    #----- Products that don't use database lookup first -----#

    ### Inverters ###
    # X64 S2
    matchResult = re.match(r"^8I64S2.+\.00X-1$", materialInput) #match if string matches format 8I64S2*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        workerStr = strPartition[0].removeprefix("8I64S2") #eliminate the prefix so we can use isolate the rest of the model number
        materialOutput = "8I64S2%s.0X-000" % (workerStr) #generate the successor model number
        swChangesRequired = False #software changes not needed
        anySuccessor = True
        directSuccessor = True

    # X64 T2
    matchResult = re.match(r"^8I64T2.+\.00X-1$", materialInput) #match if string matches format 8I64T2*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        #strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        #workerStr = strPartition[0].removeprefix("8I64T2") #eliminate the prefix so we can use isolate the rest of the model number
        #materialOutput = "8I66T2%s.0X-000" % (workerStr) #generate the successor model number (P66)
        
        swChangesRequired = True #software changes needed
        anySuccessor = True
        directSuccessor = False
        nonDirectMsg = "Transition to P66."

    # X64 T4
    matchResult = re.match(r"^8I64T4.+\.00X-1$", materialInput) #match if string starts with 8I64T4*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        workerStr = strPartition[0].removeprefix("8I64T4") #eliminate the prefix so we can use isolate the rest of the model number
        materialOutput = "8I64T4%s.0X-000" % (workerStr) #generate the successor model number
        swChangesRequired = False #software changes not needed
        anySuccessor = True
        directSuccessor = True

    # P74 S2
    matchResult = re.match(r"^8I74S2.+\.01P-1$", materialInput) #match if string matches format 8I74S2*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        workerStr = strPartition[0].removeprefix("8I74S2") #eliminate the prefix so we can use isolate the rest of the model number
        materialOutput = "8I74S2%s.0P-000" % (workerStr) #generate the successor model number
        swChangesRequired = False #software changes not needed
        anySuccessor = True
        directSuccessor = True


    # P74 T4
    matchResult = re.match(r"^8I74T4.+\.01P-1$", materialInput) #match if string matches format 8I74T4*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        workerStr = strPartition[0].removeprefix("8I74S2") #eliminate the prefix so we can use isolate the rest of the model number
        materialOutput = "8I74T4%s.0P-000" % (workerStr) #generate the successor model number
        swChangesRequired = False #software changes not needed
        anySuccessor = True
        directSuccessor = True

    # P84 T2
    matchResult = re.match(r"^8I84T2.+\.01P-1$", materialInput) #match if string matches format 8I64T2*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        #strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        #workerStr = strPartition[0].removeprefix("8I64T2") #eliminate the prefix so we can use isolate the rest of the model number
        #materialOutput = "8I66T2%s.0X-000" % (workerStr) #generate the successor model number (P66)
        
        swChangesRequired = True #software changes needed
        anySuccessor = True
        directSuccessor = False
        nonDirectMsg = "Transition to P66."

    # P84 T4
    matchResult = re.match(r"^8I84T4.+\.01P-1$", materialInput) #match if string matches format 8I64T2*.00X-1
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        #strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        #workerStr = strPartition[0].removeprefix("8I64T2") #eliminate the prefix so we can use isolate the rest of the model number
        #materialOutput = "8I66T2%s.0X-000" % (workerStr) #generate the successor model number (P66)
        
        swChangesRequired = True #software changes needed
        anySuccessor = True
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
        swChangesRequired = True #software changes needed
        anySuccessor = True
        directSuccessor = True


    ### Motors ###
    # 8LSA gen 0 -> 3
    matchResult = re.match(r"^8LSA.+-0$", materialInput) #match if string matches format 8LSA*-0
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        strPartition =  materialInput.partition("-") #break the string into pre-seperator, seperator, and post-seperator (seperator is "-")
        materialOutput = strPartition[0] + "-3"
        swChangesRequired = True #software changes needed
        anySuccessor = True
        directSuccessor = True

    # 8LSC gen 0 -> 3
    matchResult = re.match(r"^8LSC.+-0$", materialInput) #match if string matches format 8LSC*-0
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True
        strPartition =  materialInput.partition("-") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
        materialOutput = strPartition[0] + "-3"
        swChangesRequired = True #software changes needed
        anySuccessor = True
        directSuccessor = True

    # 8MSA
    matchResult = re.match(r"^8MSA.+", materialInput) #match if string matches format 8MSA*
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        swChangesRequired = True #software changes needed
        anySuccessor = True
        directSuccessor = False
        nonDirectMsg = "Go to Y:\Application\Support Team\KnowledgeBase\Hardware\Motors\MotorConversions\MSA Motor Lookup v01.1.xlsx"
    
    
    ### CompactFlash ###
    # 5CFCRD.xxxx-02
    matchResult = re.match(r"^5CFCRD\..{4}-02", materialInput) #match if string matches format*
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        dbResult = dbCursor.execute("SELECT * FROM CompactFlash")
        if dbResult != None:
            for row in dbResult:
                if row[0] == materialInput:
                    materialOutput = row[1]

        swChangesRequired = False #software changes needed
        if materialOutput != None: #if a direct replacement was found
            anySuccessor = True
            directSuccessor = True
        else:
            anySuccessor = False
            directSuccessor = False

    # 5CFCRD.xxxx-03
    matchResult = re.match(r"^5CFCRD\..{4}-03", materialInput) #match if string matches format
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        dbResult = dbCursor.execute("SELECT * FROM CompactFlash")
        if dbResult != None:
            for row in dbResult:
                if row[0] == materialInput:
                    materialOutput = row[1]

        swChangesRequired = False #software changes needed
        if materialOutput != None: #if a direct replacement was found
            anySuccessor = True
            directSuccessor = True
        else:
            anySuccessor = False
            directSuccessor = False

    # 5CFCRD.xxxx-04
    matchResult = re.match(r"^5CFCRD\..{4}-04", materialInput) #match if string matches format
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        workerStr = materialInput.removesuffix("-04") #remove "-04"
        materialOutput = workerStr + "-06" #replace with "-06"
        swChangesRequired = False #software changes needed
        anySuccessor = True
        directSuccessor = True

    # 5CFCRD.xxxx-06
    matchResult = re.match(r"^5CFCRD\..{4}-06", materialInput) #match if string matches format
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        dbResult = dbCursor.execute("SELECT * FROM CompactFlash")
        if dbResult != None:
            for row in dbResult:
                if row[0] == materialInput:
                    materialOutput = row[1]

        swChangesRequired = False #software changes needed
        if materialOutput != None: #if a direct replacement was found
            anySuccessor = True
            directSuccessor = True
        else:
            anySuccessor = False
            directSuccessor = False
    

    # 0CFCRD.xxxx.02
    matchResult = re.match(r"^0CFCRD\..{4}E\.01", materialInput) #match if string matches format*
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        dbResult = dbCursor.execute("SELECT * FROM CompactFlash")
        if dbResult != None:
            for row in dbResult:
                if row[0] == materialInput:
                    materialOutput = row[1]

        swChangesRequired = False #software changes needed
        if materialOutput != None: #if a direct replacement was found
            anySuccessor = True
            directSuccessor = True
        else:
            anySuccessor = False
            directSuccessor = False

    ### Power Panels ###
    # PP300 panels
    matchResult = re.match(r"^[4|5]PP3.+", materialInput) #match if string matches format*
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        dbResult = dbCursor.execute("SELECT * FROM PP300")
        if dbResult != None:
            for row in dbResult:
                if row[0] == materialInput:
                    materialOutput = row[1]

        swChangesRequired = True #software changes needed
        if materialOutput != None: #if a direct replacement was found
            anySuccessor = True
            directSuccessor = True
        else:
            anySuccessor = False
            directSuccessor = False

            if materialInput == "4PP352.0571-35":
                anySuccessor = True
                nonDirectMsg = "No 1:1 replacement available because of very low demand. Changeover recommendation: 5AP1151.0573-000\n"

    # PP400 panels
    matchResult = re.match(r"^4PP4.+", materialInput) #match if string matches format*
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        dbResult = dbCursor.execute("SELECT * FROM PP400")
        if dbResult != None:
            for row in dbResult:
                if row[0] == materialInput:
                    materialOutput = row[1]

        swChangesRequired = True #software changes needed
        if materialOutput != None: #if a direct replacement was found
            anySuccessor = True
            directSuccessor = True
        else:
            anySuccessor = False
            directSuccessor = False

    # PP500 panels (display), cpus and interfaces
    matchResult = re.match(r"^5PP5.+", materialInput) #match if string matches format*
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        dbResult = dbCursor.execute("SELECT * FROM PP500")
        if dbResult != None:
            for row in dbResult:
                if row[0] == materialInput:
                    materialOutput = row[1]

        swChangesRequired = True #software changes needed
        if materialOutput != None: #if a direct replacement was found
            anySuccessor = True
            directSuccessor = True
        else:
            anySuccessor = False
            directSuccessor = False

            if materialInput == "5PP552.0573-00":
                anySuccessor = True
                nonDirectMsg = "No 1:1 replacement available because of very low demand. Changeover recommendation: 5AP1151.0573-000\n"

    ### HMI ###
    # AP9xD
    matchResult = re.match(r"^5AP9\dD\..{7}", materialInput) #match if string matches format*
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        dbResult = dbCursor.execute("SELECT * FROM AP9xD")
        #dbResult = dbCursor.fetchall()
        if dbResult != None:
            for row in dbResult:
                if row[0] == materialInput:
                    materialOutput = row[1]

        swChangesRequired = True #software changes needed
        if materialOutput != None: #if a direct replacement was found
            anySuccessor = True
            directSuccessor = True
        else:
            anySuccessor = False
            directSuccessor = False

    # AP9xD Handles 
    matchResult = re.match(r"^5AC903\.HDL0-0\d", materialInput) #match if string matches format*
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        dbResult = dbCursor.execute("SELECT * FROM AP9xD")
        if dbResult != None:
            for row in dbResult:
                if row[0] == materialInput:
                    materialOutput = row[1]

        swChangesRequired = True #software changes needed
        if materialOutput != None: #if a direct replacement was found
            anySuccessor = True
            directSuccessor = True
        else:
            anySuccessor = False
            directSuccessor = False

    # AP900
    matchResult = re.match(r"^5AP9\d{2}\.\d{4}-01", materialInput) #match if string matches format*
    if matchResult != None: #if match object is not None (meaning there is at least one match)
        matchFound = True

        dbResult = dbCursor.execute("SELECT * FROM AP900")
        #dbResult = dbCursor.fetchall()
        if dbResult != None:
            for row in dbResult:
                if row[0] == materialInput:
                    materialOutput = row[1]

        swChangesRequired = True #software changes needed
        if materialOutput != None: #if a direct replacement was found
            anySuccessor = True
            directSuccessor = True
        else:
            anySuccessor = False
            directSuccessor = False
           
    ### MISC ###
    # When no other regex matches, check the misc table
    # Use Misc table for series with mixed format model numbers such as SDL3
    if matchFound == False:
        
        dbResult = dbCursor.execute("SELECT * FROM Misc")
        if dbResult != None:
            for row in dbResult:
                if row[0] == materialInput:
                    materialOutput = row[1]

        swChangesRequired = True #software changes needed
        if materialOutput != None: #if a direct replacement was found
            anySuccessor = True
            directSuccessor = True
        else:
            anySuccessor = False
            directSuccessor = False

            #if materialInput == "5PP552.0573-00":
            #    anySuccessor = True
            #    nonDirectMsg = "No 1:1 replacement available because of very low demand. Changeover recommendation: 5AP1151.0573-000\n"


    #----- Wrap Up and Output -----#
    if anySuccessor == True: #If a regex match was found
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
        #In cases that a successor could not be found there either is not a successor or there was a typo in the input
        print("Unfortunately, a successor product for the entered material number was not available. Please ensure there are no mistakes in your input.\n ") 

    

    
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
            print("Please enter a valid input (y/n). ")



