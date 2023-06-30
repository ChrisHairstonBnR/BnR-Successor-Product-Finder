import re #regular expressions
import sqlite3 #https://docs.python.org/3/library/sqlite3.html

#----- SQLite3 Setup -----#
dbConnection = sqlite3.connect("SuccessorProductDB.db")
dbCursor = dbConnection.cursor()
#dbConnection.row_factory = sqlite3.Row
dbResult = None #query result variable

class Lookup:
    def __init__(self, materialOutput, nonDirectMsg, situationalMsg, matchFound, directSuccessor, anySuccessor, validInput, swChangesRequired, customMaterial):
        self.materialOutput = materialOutput
        self.nonDirectMsg = nonDirectMsg
        self.situationalMsg = situationalMsg
        self.matchFound = matchFound
        self.directSuccessor = directSuccessor
        self.anySuccessor = anySuccessor
        self.validInput = validInput
        self.swChangesRequired = swChangesRequired
        self.customMaterial = customMaterial

def getNotes(materialInput, l: Lookup):
    notePrefix = "%s: " % materialInput   
    noteText = ''

    #----- Wrap Up and Output -----#
    if l.situationalMsg != '' and l.situationalMsg != None:
        noteText += l.situationalMsg + ' '
    elif l.customMaterial:
        noteText += "The input material is custom, please speak with the machine manufacturer for upgrade options."
    elif l.anySuccessor == True: #If any successor is available
        if l.directSuccessor == True: #if direct successor was found
            pass
        else:
            noteText += "No direct successor. %s" % (l.nonDirectMsg)
    else:
        if l.validInput:
            noteText += "The input material is valid. However, there unfortunately is no successor product."
        else:    
            #In cases there was a typo in the input, the input is not obsolete, or the material is missing from the program
            noteText += "Unfortunately, a successor product for the entered material number is not available. The entered material is either not obsolete, there are mistakes in your input or this program is missing this material. " 
    
    if noteText == '' or noteText == None:
        outputNotes = ''
    else:
        outputNotes = notePrefix + noteText

    return outputNotes



def getSuccessor(materialInput):
        materialInput = materialInput.strip() #remove whitespace from front and back
        #print("Finding successor product for %s... " % (materialInput)); #formatted string
        #print("(Please note that this program does not check if the material number entered is actually obsolete or real.)\n") #disclaimer
        
        #Reset variables for new loop
        materialOutput = '' 
        nonDirectMsg = '' 
        situationalMsg = '' 
        matchFound = False 
        directSuccessor = False 
        anySuccessor = False 
        validInput = False
        swChangesRequired = False
        customMaterial = False

        # Check if material is custom
        hyphenFindResult = str(materialInput).find('-')
        if hyphenFindResult != -1:
            if str(materialInput).split('-')[1][0] == 'K' or str(materialInput).split('-')[1][0] == 'C':
                customMaterial = True
        else: 
            pass



        #----- Core Lookup Code -----#

        ### Drives/Inverters ###
        # X64 S2
        matchResult = re.match(r"^8I64S2.{5}\.00[X|0]-1$", materialInput) #match if string matches format 8I64S2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
            workerStr = strPartition[0].removeprefix("8I64S2") #eliminate the prefix so we can use isolate the rest of the model number
            materialOutput = "8I64S2%s.0X-000 + 8I66S2%s.00-000" % (workerStr, workerStr) #generate the successor model numbers for base device and communication card
            anySuccessor = True
            directSuccessor = True
            situationalMsg = 'The base device and communication card %s must be ordered together.' % (materialOutput)

        # X64 T2
        matchResult = re.match(r"^8I64T2.+\.00[X|0]-1$", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
            workerStr = strPartition[0].removeprefix("8I64T2") #eliminate the prefix so we can use isolate the rest of the model number
            materialOutput = "8I64T2%s.0X-000 + 8I66T2%s.00-000" % (workerStr, workerStr) #generate the successor model numbers for base device and communication card
            anySuccessor = True
            directSuccessor = True
            situationalMsg = 'The base device and communication card %s must be ordered together.' % (materialOutput)


            #if strPartition[2][2] == 'X':
            #    swChangesRequired = True #software changes needed
            #    anySuccessor = True
            #    directSuccessor = False
            #    nonDirectMsg = "Transition to P66."
            #else:
            #    situationalMsg = 'The material numbered entered is the base module for the ACOPOS inverter and is still in production. Please enter the 8I64T2xxxxx.00X-1 material number.'

        # X64 T4
        matchResult = re.match(r"^8I64T4.+\.00[X|0]-1$", materialInput) #match if string starts with 8I64T4*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
            workerStr = strPartition[0].removeprefix("8I64T4") #eliminate the prefix so we can use isolate the rest of the model number
            materialOutput = "8I64T4%s.0X-000 + 8I66T4%s.00-000" % (workerStr, workerStr) #generate the successor model numbers for base device and communication card
            anySuccessor = True
            directSuccessor = True
            situationalMsg = 'The base device and communication card %s must be ordered together.' % (materialOutput)
            
            
        # P74 S2
        matchResult = re.match(r"^8I74S2.+\.01[P|0]-1$", materialInput) #match if string matches format 8I74S2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
            workerStr = strPartition[0].removeprefix("8I74S2") #eliminate the prefix so we can use isolate the rest of the model number
            materialOutput = "8I74S2%s.0X-000 + 8I76S2%s.00-000" % (workerStr, workerStr) #generate the successor model numbers for base device and communication card
            anySuccessor = True
            directSuccessor = True
            situationalMsg = 'The base device and communication card %s must be ordered together.' % (materialOutput)

        # P74 T4
        matchResult = re.match(r"^8I74T4.+\.01[P|0]-1$", materialInput) #match if string matches format 8I74T4*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
            workerStr = strPartition[0].removeprefix("8I74T4") #eliminate the prefix so we can use isolate the rest of the model number
            materialOutput = "8I74S2%s.0X-000 + 8I76S2%s.00-000" % (workerStr, workerStr) #generate the successor model numbers for base device and communication card
            anySuccessor = True
            directSuccessor = True
            situationalMsg = 'The base device and communication card %s must be ordered together.' % (materialOutput)

        # P84 T2
        matchResult = re.match(r"^8I84T2.+\.01[P|0]-1$", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
            workerStr = strPartition[0].removeprefix("8I84T2") #eliminate the prefix so we can use isolate the rest of the model number
            swChangesRequired = True #software changes needed
            anySuccessor = True
            directSuccessor = False
            nonDirectMsg = "Transition to P66."
           

        # P84 T4
        matchResult = re.match(r"^8I84T4.+\.01[P|0]-1$", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
            workerStr = strPartition[0].removeprefix("8I64T2") #eliminate the prefix so we can use isolate the rest of the model number
            swChangesRequired = True #software changes needed
            anySuccessor = True
            directSuccessor = False
            nonDirectMsg = "Transition to P66 or P86 depending on performance needed."
            

        # ACOPOS 8V
        matchResult = re.match(r"^8V1\d{3}\.\d{2}-\d", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
        
            swChangesRequired = True #software changes needed
            anySuccessor = True
            directSuccessor = False
            nonDirectMsg = "Transition to the ACOPOS P3 or ACOPOSmulti series."
        
        #ACOPOS Plug in Cards
        matchResult = re.match(r"^8AC\d{3}\.\d{2}-\d", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            dbResult = dbCursor.execute("SELECT * FROM 'ACOPOS Plugin'")
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True


            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False
        
        # ACOPOSmulti
        matchResult = re.match(r"^8BVI\d{4}H.{3}\.\d{3}-1", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM ACOPOSmulti")
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True


            swChangesRequired = False #software changes not needed, check SN20/2020
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False
        
        # ACOPOSinverter Plugin
        matchResult = re.match(r"^8I0AC123\.\d{3}-\d", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            
            swChangesRequired = True #software changes needed
            anySuccessor = True
            directSuccessor = False
            nonDirectMsg = "The appropriate successor will be one of the P86 8I0IFENC.xxx-1 encoder interfaces."

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
        
        ### Other Motion ###
        # 8B0F0160H000.A00-1
        matchResult = re.match(r"8B0F0160H000.A00-1", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            materialOutput = "8B0F0160H000.000-1"
            swChangesRequired = True #software changes needed
            anySuccessor = True
            directSuccessor = True

        

        ### CompactFlash ###
        # 5CFCRD.xxxx-02
        matchResult = re.match(r"^5CFCRD\..{4}-02", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM CompactFlash")
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = False #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
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
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = False #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
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
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = False #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
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
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = False #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False

        ### Memory ###
        matchResult = re.match(r"^5MMDDR\.\d{4}-0\d", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM Memory")
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = False #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
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
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
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
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
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
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False

                if materialInput == "5PP552.0573-00":
                    anySuccessor = True
                    nonDirectMsg = "No 1:1 replacement available because of very low demand. Changeover recommendation: 5AP1151.0573-000\n"

        # PP45 (device)
        matchResult = re.match(r"^4PP045\.\d{4}-.+", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = True
            directSuccessor = False
            swChangesRequired = True #software changes needed
            nonDirectMsg = 'The listed successor is the Power Panel 65 series. However, that series is also obsolete. Transition to a Power Panel C-Series device or a Power Panel T30 with a X20CP Compact-S depending on demands of the application. See sales notice 38/2021.'

        # PP45 (interfaces)
        matchResult = re.match(r"^4PP045\.IF.+", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = True
            directSuccessor = False
            swChangesRequired = True #software changes needed
            validInput = True
            nonDirectMsg = "Look into the appropriate interfaces for the system you are upgrading to. Speak with a sales representative to determine the best upgrade for the application."

        # PP65 (device)
        matchResult = re.match(r"^4PP065\.\d{4}-.{3}", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = True
            directSuccessor = False
            swChangesRequired = True #software changes needed
            nonDirectMsg = 'Transition to a Power Panel C-Series device or a Power Panel T30 with a X20CP Compact-S depending on demands of the application. See sales notice 38/2021.'

        # PP65 (interfaces)
        matchResult = re.match(r"^4PP065\.IF\d{2}-1", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = True
            directSuccessor = False
            swChangesRequired = True #software changes needed
            validInput = True
            nonDirectMsg = "Look into the appropriate interfaces for the system you are upgrading to. Speak with a sales representative to determine the best upgrade for the application."


        ### HMI ###
        # AP9xD
        matchResult = re.match(r"^5AP9\dD\..{7}", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM AP9xD")
            #dbResult = dbCursor.fetchall()
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
                situationalMsg = "Software changes are not necessary if the panel is connected to an APC via SDL."
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
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = False #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
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
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
                situationalMsg = "Software changes are not necessary if the panel is connected to an APC via SDL."
            else:
                anySuccessor = False
                directSuccessor = False

        # MP712x
        matchResult = re.match(r"^5MP712[0|1]\..{4}-000", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            swChangesRequired = True #software changes needed
            anySuccessor = False
            directSuccessor = False
            validInput = True
            #materialOutput = ''

        # 5MP7151.101E-001
        matchResult = re.match(r"^5MP7151.101E-001", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            swChangesRequired = True #software changes needed
            anySuccessor = False
            directSuccessor = False
            validInput = True
            #materialOutput = ''

        # MP50
        matchResult = re.match(r"^5MP050\.0653-\d{2}$", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            #strPartition =  materialInput.partition(".") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
            #workerStr = strPartition[0].removeprefix("8I64T2") #eliminate the prefix so we can use isolate the rest of the model number
            #materialOutput = "8I66T2%s.0X-000" % (workerStr) #generate the successor model number (P66)
            
            swChangesRequired = True #software changes needed
            anySuccessor = True
            directSuccessor = False
            nonDirectMsg = "The possibilities for use of the MP7100 must be checked individually.Speak with a sales representative to determine the best upgrade for the application."



        ### PCs ####
        # PPC300
        matchResult = re.match(r"5PC310\.L800-00", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            materialOutput = "5PPC2100.BY01-000"
            swChangesRequired = True #software changes needed
            anySuccessor = True
            directSuccessor = True

        # PC5xx (system units)
        matchResult = re.match(r"^5PC51[0|1]\.SX01-00", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM PC5xx")
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False
                
        # PC5xx (cpus)
        matchResult = re.match(r"^5PP5CP\.US15-\d{2}", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM PC5xx")
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False


        # PC5xx Interfaces
        matchResult = re.match(r"^5PP5IF\..{4}-00", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = True
            directSuccessor = False
            swChangesRequired = True
            nonDirectMsg = "Look into the appropriate interfaces for the system you are upgrading to. Speak with a sales representative to determine the best upgrade for the application."

        # PC5xx I/O
        matchResult = re.match(r"^5PP5IO\.G[M|N]AC-00", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = True
            directSuccessor = False
            swChangesRequired = True
            nonDirectMsg = "Changing over the I/O board is dependent on the interfaces used. Speak with a sales representative to determine the best upgrade for the application."

                

        # PC6xx
        matchResult = re.match(r"^5PC600\..{4}-\d{2}", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM PC6xx")
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False

        # PC7xx
        matchResult = re.match(r"^5PC7\d{2}\..{4}-\d{2}", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM PC7xx")
            #dbResult = dbCursor.fetchall()
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False
                if materialInput == "5PC725.1505-00" or materialInput == "5PC725.1505-01":
                    anySuccessor = True
                    nonDirectMsg = "Panel PC 725 units can be replaced by the combination of the support arm variant of the Automation Panel 900 and the new Panel PC based on Intel Bay Trail technology."


        # PC8xx
        matchResult = re.match(r"^5PC8\d{2}\..{4}-\d{2}", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM PC8xx")
            #dbResult = dbCursor.fetchall()
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False

        # PC9xx
        matchResult = re.match(r"^5PC900\.TS77-\d{2}", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            
            swChangesRequired = True #software changes needed
            anySuccessor = True
            directSuccessor = False
            nonDirectMsg = "Transition to the appropriate TS17 (5PC900.TS17-xx) CPU board depending on performance needed."

        # PC 6xx+ Accessories
        matchResult = re.match(r"^5AC\d{3}\..{4}-\d{2}", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = True
            directSuccessor = False
            dotSplit = str(materialInput).split('.')
            if dotSplit[1][0:2] == 'HS':
                nonDirectMsg = "The appropriate heatsink will be associated with the successor PC. Speak with a sales representative to determine the best upgrade for the application."
                swChangesRequired = False
            elif dotSplit[1][0:3] == 'HDD':
                nonDirectMsg = "The appropriate hard drive is dependent on the successor PC. Speak with a sales representative to determine the best upgrade for the application."
                swChangesRequired = False
            elif dotSplit[1][0:3] == 'SSD':
                nonDirectMsg = "The appropriate solid state drive is dependent on the successor PC. Speak with a sales representative to determine the best upgrade for the application."
                swChangesRequired = False
            elif dotSplit[1][0:2] == 'DV':
                nonDirectMsg = "The appropriate DVD drive will be associated with the successor PC. Speak with a sales representative to determine the best upgrade for the application."
                swChangesRequired = False
            elif dotSplit[1][0:2] == 'FA':
                nonDirectMsg = "The appropriate fan will be associated with the successor PC. Speak with a sales representative to determine the best upgrade for the application."
                swChangesRequired = False
            elif dotSplit[1][1:4] == 'RAM':
                nonDirectMsg = "'The appropriate memory option is dependent on the successor PC. Speak with a sales representative to determine the best upgrade for the application."
                swChangesRequired = False
            elif dotSplit[1][3] == 'X':
                nonDirectMsg = "'The appropriate labels are dependent on the successor PC. Speak with a sales representative to determine the best upgrade for the application."
                swChangesRequired = False
            else:
                nonDirectMsg = 'The appropriate successor is dependent on the successor PC. Speak with a sales representative to determine the best upgrade for the application.'
                swChangesRequired = True

            # OLD CODE    
            # dbResult = dbCursor.execute("SELECT * FROM 'PC Accessories'")
            # if dbResult != None:
            #     for row in dbResult:
            #         if str(row[0]).strip() == materialInput:
            #             materialOutput = row[1]
            #             validInput = True

            # swChangesRequired = False
            # if materialOutput != None and materialOutput != '': #if a direct replacement was found
            #     anySuccessor = True
            #     directSuccessor = True
            #     if materialOutput == '5AC901.HS00-01':
            #         situationalMsg = 'This successor is intended for the TS-17 (QM170/HM170) system units.'

            # else:
            #     anySuccessor = False
            #     directSuccessor = False

        ### PC Configurations ###
        matchResult = re.match(r"^5[A-Z].{12}-\d{3}", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            situationalMsg = "The material number entered was for a configuration. Speak with a sales representative to determine the best upgrade for the application."
        

        ### Safety PLCs ###
        # X20SL80xx
        matchResult = re.match(r"^X20SL80.{2}$", materialInput) #match if matches format X20SL80xx
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            strPartition =  materialInput.partition("80") #break the string into pre-seperator, seperator, and post-seperator (seperator is ".")
            materialOutput = "X20SL81%s" % (strPartition[2]) #generate the successor P64new model number
            swChangesRequired = True #software changes needed
            anySuccessor = True
            directSuccessor = True
        
        ### GPOS ####
        # Windows
        matchResult = re.match(r"^5SWW.+", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            situationalMsg = "The material number entered was for a Windows operating system. It's successor operating system is dependent on the compatibility of the target PC."

        # Linux
        matchResult = re.match(r"^5SWLIN.+", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            situationalMsg = "The material number entered was for a Linux operating system. It's successor operating system is dependent on the compatibility of the target PC."

        ### X2X ###
        # X20 Umbrella
        matchResult = re.match(r"^X20.+", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM X20")
            #dbResult = dbCursor.fetchall()
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False
                if materialInput == "X20CP1483":
                    anySuccessor = True
                    nonDirectMsg = "The Compact-S PLC series is the ideal successor."
                elif materialInput == "X20CP1301" or materialInput == "X20CP1381" or materialInput == "X20CP1382" or materialInput == "X20CP1381-RT" or materialInput == "X20CP1382-RT":
                    anySuccessor = True
                    nonDirectMsg = "Look at X20 PLCs for the appropriate successor. Speak with a sales representative to determine the best fit for the application."

        # X67 Umbrella
        matchResult = re.match(r"^X67.+", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM X67")
            #dbResult = dbCursor.fetchall()
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False


        

        ### Cables ###
        # 5CAxxx.xxxx-xx Cables (AP800, APC/PPC, etc.)
        matchResult = re.match(r"^5CA.{3}\.\d{4}-\d{2}", materialInput) #match if string matches format*
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True

            dbResult = dbCursor.execute("SELECT * FROM Cables")
            #dbResult = dbCursor.fetchall()
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False

        ### Other Systems ###
        # B&R 2003
        matchResult = re.match(r"^7.{2}\d{3}\.\d", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = False
            directSuccessor = False
            situationalMsg = "The B&R 2003 system is too outdated to provide a comparable successor. Projects should be changed over to X20."

        matchResult = re.match(r"^7.{2}\d{3}\.\d{2}-\d", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = False
            directSuccessor = False
            situationalMsg = "The B&R 2003 system is too outdated to provide a comparable successor. Projects should be changed over to X20."

        # B&R 2005
        matchResult = re.match(r"^3.{2}\d{3}\.\d", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = False
            directSuccessor = False
            situationalMsg = "The B&R 2005 system is too outdated to provide a comparable successor. Projects should be changed over to X20."

        matchResult = re.match(r"^3.{2}\d{3}\.\d{2}-\d", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = False
            directSuccessor = False
            situationalMsg = "The B&R 2005 system is too outdated to provide a comparable successor. Projects should be changed over to X20."

        # B&R 2010
        matchResult = re.match(r"^2.{2}\d{3}\.\d", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = False
            directSuccessor = False
            situationalMsg = "The B&R 2010 system is too outdated to provide a comparable successor. Projects should be changed over to X20."

        matchResult = re.match(r"^2.{2}\d{3}\.\d{2}-\d", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = False
            directSuccessor = False
            situationalMsg = "The B&R 2010 system is too outdated to provide a comparable successor. Projects should be changed over to X20."

        # PROVIT
        matchResult = re.match(r"^5C2\d{3}\.\d{2}", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = False
            directSuccessor = False
            situationalMsg = "The PROVIT system is too outdated to provide a comparable successor. Projects should be changed over to X20."

        matchResult = re.match(r"^5C3\d{3}\.\d", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = False
            directSuccessor = False
            situationalMsg = "The PROVIT system is too outdated to provide a comparable successor. Projects should be changed over to X20."



        # Interfaces (must go after 2003, 2005 and 2010 so that it can overwrite)
        matchResult = re.match(r"^.IF\d{3}\.\d", materialInput) #match if string matches format 8I64T2*.00X-1
        if matchResult != None: #if match object is not None (meaning there is at least one match)
            matchFound = True
            anySuccessor = True
            directSuccessor = False
            nonDirectMsg = "Look into the appropriate interfaces for the system you are upgrading to. Speak with a sales representative to determine the best fit for the application."
            
        ### MISC ###
        # When no other regex matches, check the misc table
        # Use Misc table for series with mixed format model numbers such as SDL3
        if matchFound == False:
            
            dbResult = dbCursor.execute("SELECT * FROM Misc")
            if dbResult != None:
                for row in dbResult:
                    if str(row[0]).strip() == materialInput:
                        materialOutput = row[1]
                        validInput = True

            swChangesRequired = True #software changes needed
            if materialOutput != None and materialOutput != '': #if a direct replacement was found
                anySuccessor = True
                directSuccessor = True
            else:
                anySuccessor = False
                directSuccessor = False

                #if materialInput == "5PP552.0573-00":
                #    anySuccessor = True
                #    nonDirectMsg = "No 1:1 replacement available because of very low demand. Changeover recommendation: 5AP1151.0573-000\n"

        return Lookup(materialOutput, nonDirectMsg, situationalMsg, matchFound, directSuccessor, anySuccessor, validInput, swChangesRequired, customMaterial)