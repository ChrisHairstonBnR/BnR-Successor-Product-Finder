import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import numpy as np
from guiFun import *
from lookup import *
import webbrowser
import settings


#----- VERSION -----#
sofwareVersion = '0.5b'

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



#print("***WELCOME TO THE B&R SUCCESSOR PRODUCT FINDER v%s***\nWritten by Chris Hairston" % sofwareVersion);


def selectTheme():
    root.set_theme(theme_name=optionTheme.get(), themebg= True, toplevel= True)
    button_github_link.config(bg= root['background'], fg= invertHexColor(root['background']))
    initSettings.setDefaultTheme(optionTheme.get())

def closeApp():
    root.quit()


#Triggers when search button is clicked
def on_button_click():
    rawInput = entry_obsolete_part.get('1.0', tk.END)
    rawInput = str(rawInput).upper() #convert input to uppercase
    materialInputList = rawInput.split()

    #clear current outputs
    text_successor_output.config(state= 'normal')
    text_successor_output.delete('1.0', tk.END)
    text_successor_output.config(state= 'disabled')

    text_sw_changes_required.config(state= 'normal')
    text_sw_changes_required.delete('1.0', tk.END)
    text_sw_changes_required.config(state= 'disabled')

    text_successor_notes.config(state= 'normal')
    text_successor_notes.delete('1.0', tk.END)
    text_successor_notes.config(state= 'disabled')


    for materialInput in materialInputList:
        lookupResult = getSuccessor(materialInput)

        #label_successor_part.config(text=successor_part)

        #keep material output
        materialOutput = lookupResult.materialOutput
        if materialOutput == '' or materialOutput == None:
            materialOutput = 'N/A'

        #format the output to clearly show input and successor
        outputSuccessor = '%s -> %s' % (materialInput, materialOutput)

        #Output Note
        outputNote = getNotes(materialInput, lookupResult)

        #Sw changes required output
        if lookupResult.swChangesRequired:
            outputSwChanges = '%s: yes' % materialInput
        else:
            outputSwChanges = '%s: no' % materialInput

        #append text outputs
        text_successor_output.config(state= 'normal')
        text_successor_output.insert(tk.END, outputSuccessor + '\n')
        text_successor_output.config(state= 'disabled')
        text_sw_changes_required.config(state= 'normal')
        text_sw_changes_required.insert(tk.END, outputSwChanges + '\n')
        text_sw_changes_required.config(state= 'disabled')
        if outputNote != '' and outputNote != None:
            text_successor_notes.config(state= 'normal')
            text_successor_notes.insert(tk.END, outputNote + '\n')
            text_successor_notes.config(state= 'disabled')
    
    #final note to append
    text_successor_notes.config(state= 'normal')
    text_successor_notes.insert(tk.END, 'Please ensure successor(s) is (are) not obsolete too.')
    text_successor_notes.config(state= 'disabled')




def on_github_link_click():
    webbrowser.open_new_tab('https://github.com/ChrisHairstonBnR/Python-Successor-Finder/issues')

#----- GUI -----#
initSettings = settings.appSettings()


# Create the main window
root = ThemedTk(theme=initSettings.defaultTheme, toplevel= True, themebg=True)
#root.config(theme= 'black')
root.title("BnR SPF v%s" % sofwareVersion)

optionTheme = tk.StringVar(value=initSettings.defaultTheme)
themeList = ['Light', 'Dark']
optionThemeList = root.get_themes()
optionThemeList.sort()



# Menu Setup
menubar = tk.Menu(root)
optionMenu = tk.Menu(menubar, tearoff=0)
themeMenu = tk.Menu(optionMenu, tearoff=0)
for theme in optionThemeList:
    themeMenu.add_radiobutton(label=theme.capitalize(), variable=optionTheme, value=theme, command=selectTheme)

optionMenu.add_cascade(label="Theme", menu=themeMenu)
optionMenu.add_separator()
optionMenu.add_command(label="Exit", command=closeApp)

menubar.add_cascade(label="Options", menu=optionMenu)


# Create the GUI widgets
label_obsolete_part = ttk.Label(root, text="Obsolete Part Number(s):")
entry_obsolete_part = tk.Text(root, height= 10, width= 15)
button_search = ttk.Button(root, text="Search", command=on_button_click)
label_successor_part = ttk.Label(root, text="Successor Part Number(s):")
text_successor_output = tk.Text(root, height= 10, width= 40, bg='#D3D3D3')
label_successor_notes = ttk.Label(root, text= "Notes:")
text_successor_notes = tk.Text(root, height = 10, width= 50, bg="#FFFDD0")
button_github_link = tk.Button(root, text= "To report an issue or missing material, create an issue at https://github.com/ChrisHairstonBnR/Python-Successor-Finder/issues or click here.", command=on_github_link_click, border=0, bg=root['background'], fg=invertHexColor(root['background']))
notes_scrollbar = ttk.Scrollbar(root, orient='horizontal')
output_scrollbar = ttk.Scrollbar(root, orient='horizontal')
label_sw_changes_required = ttk.Label(root, text= "Software Changes Required?")
text_sw_changes_required = tk.Text(root, height= 10, width= 20)


#Widget configuration
text_successor_notes.config(xscrollcommand=notes_scrollbar.set, wrap="none", state= 'disabled')
text_successor_output.config(xscrollcommand=output_scrollbar.set, state= 'disabled', wrap='none') #Set text boxes as read only
text_sw_changes_required.config(state='disabled', wrap='none')
notes_scrollbar.config(command=text_successor_notes.xview)
output_scrollbar.config(command=text_successor_output.xview)
button_github_link.config()
root.config(menu= menubar)



# Position the widgets using the grid geometry manager
label_obsolete_part.grid(row=0, column=0, padx=5, pady=5)
entry_obsolete_part.grid(row=1, column=0, padx=5, pady=5)
button_search.grid(row=2, column=0, columnspan=1, padx=5, pady=5)
label_successor_part.grid(row=0, column=1, padx=5, pady=5)
text_successor_output.grid(row=1, column=1, padx=5, pady=5)
label_successor_notes.grid(row=0, column=3, padx=5, pady=5)
text_successor_notes.grid(row=1, column=3, padx=5, pady=5)
button_github_link.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='e')
notes_scrollbar.grid(row=2, column=3, sticky='ew')
output_scrollbar.grid(row=2, column=1, sticky='ew')
label_sw_changes_required.grid(row=0, column=2, padx=5, pady=5)
text_sw_changes_required.grid(row=1, column=2, padx=5, pady=5)


# Start the main loop
root.mainloop()




# while runAgainBool == True: #core code is in while loop so user can do lookup as many times as desired
#     #----- Get User Input -----#
#     rawInput = input("Please enter the material number(s) of the obsolete parts (multiple parts can be seperated by commas) \n(PC configurations must be broken down into individual component materials)\n") #user input
#     rawInput = str(rawInput).upper() #convert input to uppercase
#     materialInputList = rawInput.split(",")
#     for materialInput in materialInputList:

#         lookupResult = getSuccessor(materialInput)
        
#         materialOutput = lookupResult.materialOutput
#         nonDirectMsg = lookupResult.nonDirectMsg
#         situationalMsg = lookupResult.situationalMsg
#         matchFound = lookupResult.matchFound
#         directSuccessor = lookupResult.directSuccessor
#         anySuccessor = lookupResult.anySuccessor
#         validInput = lookupResult.validInput

#         #----- Wrap Up and Output -----#
#         if situationalMsg != '' and situationalMsg != None:
#             print(situationalMsg) 
#         elif anySuccessor == True: #If any successor is available
#             if directSuccessor == True: #if direct successor was found
#                 print("The replacement material number(s) is (are):\n%s" % (materialOutput)) #print output
                
#             else:
#                 print("No direct successor found. %s\n" % (nonDirectMsg))

#             print("(Please ensure that this successor is not obsolete itself.)\n") #disclaimer

#             if swChangesRequired == True: #if software changes are required
#                 print("Software changes will be necessary in Automation Studio.\n")
#             else: 
#                 print("No software changes required.\n")
#         else:
#             if validInput:
#                 print("The input material appears to be valid. However, there unfortunately is no successor product.")
#             else:    
#                 #In cases there was a typo in the input, the input is not obsolete, or the material is missing from the program
#                 print("Unfortunately, a successor product for the entered material number is not available. The entered material is either not obsolete, there are mistakes in your input or this program is missing this material.\n ") 


#     print("To report an issue or missing material, create an issue at https://github.com/ChrisHairstonBnR/Python-Successor-Finder/issues\n")
  
#     #----- Go Again? -----#
#     validRunAgainInput = False
#     while validRunAgainInput == False:
#         runAgainInput = input("Would you like to enter another (more) material number(s)? (y/n)\n")
#         if runAgainInput == 'Y' or runAgainInput == 'y':
#             validRunAgainInput = True
#             runAgainBool = True
#         elif runAgainInput == 'N' or runAgainInput == 'n':
#             validRunAgainInput = True
#             runAgainBool = False
#         else:
#             validRunAgainInput = False
#             print("Please enter a valid input (y/n). ")



