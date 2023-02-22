import re #regular expressions
import sqlite3 #https://docs.python.org/3/library/sqlite3.html

materialInput = ''
materialInput = input("Please enter the material number of the obsolete part\n") #user input
materialInput = str(materialInput).upper() #convert input to uppercase
materialInput = materialInput.strip() #remove whitespace from front and back
print("Finding successor product for %s...\n" % (materialInput)); #formatted string

#output variable declaration
materialOutput = '';
swChangesRequired = False

#----- Regex Cheat Sheet -----#
# "^": Start of line/string
# "\.": escape input to use "."
# ".": matches any character (except for line terminators)
# "+": matches the previous token between one and unlimited times

#----- Products that don't use database lookup first -----#
workerStr = ''; #used for string manipulation operations


### Inverters ###

# P64 S2
matchResult = re.match(r"^8I64S2.+\.00X-1$", materialInput) #match if string matches format 8I64S2*.00X-1
if matchResult != None: #if match object is not None (meaning there is at least one match)
    #code here
    strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
    workerStr = strPartition[0].removeprefix("8I64S2") #eliminate the prefix so we can use isolate the rest of the model number
    materialOutput = "8I64S2%s.0X-000" % (workerStr) #generate the successor model number
    swChangesRequired = False; #software changes not needed


# P64 T4
matchResult = re.match(r"^8I64T4.+\.00X-1$", materialInput) #match if string starts with 8I64T4*.00X-1
if matchResult != None: #if match object is not None (meaning there is at least one match)
    #code here
    strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
    workerStr = strPartition[0].removeprefix("8I64T4") #eliminate the prefix so we can use isolate the rest of the model number
    materialOutput = "8I64T4%s.0X-000" % (workerStr) #generate the successor model number
    swChangesRequired = False; #software changes not needed

# P74 S2
matchResult = re.match(r"^8I74S2.+\.01P-1$", materialInput) #match if string matches format 8I74S2*.00X-1
if matchResult != None: #if match object is not None (meaning there is at least one match)
    #code here
    strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
    workerStr = strPartition[0].removeprefix("8I74S2") #eliminate the prefix so we can use isolate the rest of the model number
    materialOutput = "8I74S2%s.0P-000" % (workerStr) #generate the successor model number
    swChangesRequired = False; #software changes not needed


# P74 T4
matchResult = re.match(r"^8I74T4.+\.01P-1$", materialInput) #match if string matches format 8I74T4*.00X-1
if matchResult != None: #if match object is not None (meaning there is at least one match)
    #code here
    strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
    workerStr = strPartition[0].removeprefix("8I74S2") #eliminate the prefix so we can use isolate the rest of the model number
    materialOutput = "8I74T4%s.0P-000" % (workerStr) #generate the successor model number
    swChangesRequired = False; #software changes not needed


### Safety PLCs ###
# X20SL80xx
matchResult = re.match(r"^X20SL80.{2}$", materialInput) #match if matches format X20SL80xx
if matchResult != None: #if match object is not None (meaning there is at least one match)
    #code here
    strPartition =  materialInput.partition("80") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
    workerStr = strPartition[0].removeprefix("8I64S2") #eliminate the prefix so we can use isolate the rest of the model number
    materialOutput = "X20SL81%s" % (strPartition[2]) #generate the successor P64new model number
    swChangesRequired = True; #software changes not needed


#----- Wrap Up and Output -----#
if materialOutput != '': #If a successor was found
    print("The replacement material number is %s\n" % (materialOutput)) #print output

    if swChangesRequired == True:
        print("Software changes will be necessary in Automation Studio.\n")
    else: 
        print("No software changes required.\n")

else:
    #In cases that a successor could not be found there either is not a successor or there was a typo in the input
    print("Unfortunately, there is no successor product for the entered material number. Please ensure there are no mistakes in your input.\n ") 

