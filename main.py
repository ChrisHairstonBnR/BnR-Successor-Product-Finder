import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import numpy as np
from guiFun import *
from lookup import *
import webbrowser
import settings
from update import *


#----- VERSION -----#
sofwareVersion = '0.85b'
updateAvailable = False
offlineMode = False
hasLatestVersion = False
hasDevVersion = False



def selectTheme():
    # Because root is ThemedTk, changing the theme is simple
    root.set_theme(theme_name=optionTheme.get(), themebg= True, toplevel= True)
    button_github_link.config(bg= root['background'], fg= invertHexColor(root['background'])) #manually change the issue link text colors
    initSettings.setDefaultTheme(optionTheme.get()) #change setting in settings.ini file

def resetDefaults():
    #Simply call the default settings function
    resetResponse = messagebox.showwarning ('Reset All Setting to Default?', 'Are you sure you would like to restore all settings to default?', type = 'yesno')
    if resetResponse == True or resetResponse == 'yes':
        initSettings.restoreDefaultSettings()
        root.set_theme(theme_name=initSettings.defaultTheme, themebg= True, toplevel= True)
        button_github_link.config(bg= root['background'], fg= invertHexColor(root['background'])) #manually change the issue link text colors
        root.update()
    else:
        pass

def prefChange():
    initSettings.showInputInOutput = menuShowInputInOutput.get()
    initSettings.showInputInNotes = menuShowInputInNotes.get()
    initSettings.saveSettings()

def closeApp():
    root.quit()


def syncScroll(*args):
    #Syncronizes the scroll between the 4 panes
    entry_obsolete_part.yview('moveto', args[0])
    text_successor_output.yview('moveto', args[0])
    text_sw_changes_required.yview('moveto', args[0])
    text_successor_notes.yview('moveto', args[0])

    vertical_scrollbar.set(*args)


def openAbout():

    def closeAbout():
        child_about.destroy()
    
    def clickUpdate():
        webbrowser.open_new_tab(u.latestVersionLink)

    #Define and place "About" window elements
    child_about = tk.Toplevel(root)
    child_about.title("About BnR SPF")
    child_about.grab_set()
    if hasLatestVersion:
        aboutTextTop = "BnR SPF\nVersion: %s (Latest)\n" % sofwareVersion
    elif hasDevVersion:
        aboutTextTop = "BnR SPF\nVersion: %s (Development)\n" % sofwareVersion
    else: aboutTextTop = "BnR SPF\nVersion: %s\n" % sofwareVersion
    label_child_top = ttk.Label(child_about, text=aboutTextTop)
    label_child_top.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    aboutTextBot = 'Created By: Chris Hairston \nhttps://github.com/ChrisHairstonBnR/Python-Successor-Finder/'
    label_child_bot = ttk.Label(child_about, text=aboutTextBot)
    label_child_bot.grid(row=1, column=0, columnspan=2,  padx=5, pady=5, sticky='w')
    button_close_child = ttk.Button(child_about, text='OK', command=closeAbout)
    button_close_child.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    button_update_child = ttk.Button(child_about, text="Download Update", command=clickUpdate)
    button_update_child.grid(row=0, column=1, padx=5, pady=5)

    if not updateAvailable:
        button_update_child.config(state='disabled')
    

def clearAll(clearEntry: bool):
    #Used to clear all output panes (and optionally input pane)
    if clearEntry:
        entry_obsolete_part.delete('1.0', tk.END)

    text_successor_output.config(state= 'normal') #must enable output to change and then redisable after
    text_successor_output.delete('1.0', tk.END) #clear output materials
    text_successor_output.config(state= 'disabled')

    text_sw_changes_required.config(state= 'normal') #must enable output to change and then redisable after
    text_sw_changes_required.delete('1.0', tk.END) #clear software changes panel
    text_sw_changes_required.config(state= 'disabled')

    text_successor_notes.config(state= 'normal') #must enable output to change and then redisable after
    text_successor_notes.delete('1.0', tk.END) #clear notes
    text_successor_notes.config(state= 'disabled')

#Triggers when search button is clicked
def on_button_click():
    rawInput = entry_obsolete_part.get('1.0', tk.END)
    rawInput = str(rawInput).upper() #convert input to uppercase
    materialInputList = rawInput.split()

    #clear current outputs
    clearAll(clearEntry=False)


    for materialInput in materialInputList:
        lookupResult = getSuccessor(materialInput)

        #label_successor_part.config(text=successor_part)

        #keep material output
        materialOutput = lookupResult.materialOutput
        if materialOutput == '' or materialOutput == None:
            materialOutput = 'N/A'

        #format the output to clearly show input and successor
        if initSettings.showInputInOutput:
            outputSuccessor = '%s -> %s' % (materialInput, materialOutput)
        else:
            outputSuccessor = materialOutput

        #Output Note
        outputNote = getNotes(lookupResult)
        if initSettings.showInputInNotes:
            notePrefix = '%s: ' % materialInput
            if outputNote == '' or outputNote == None:
                formatNote = ''
            else:
                formatNote = notePrefix + outputNote
        else:
            if outputNote == '' or outputNote == None:
                formatNote = ''
            else:
                formatNote = outputNote

        if materialOutput == 'N/A' and not lookupResult.swChangesRequired :
            #outputSwChanges = '%s: N/A' % materialInput
            outputSwChanges = 'N/A'
        elif lookupResult.swChangesRequired:
            outputSwChanges = 'yes'
        else:
            outputSwChanges = 'no'

        #append text outputs
        text_successor_output.config(state= 'normal')
        text_successor_output.insert(tk.END, outputSuccessor + '\n')
        text_successor_output.config(state= 'disabled')
        text_sw_changes_required.config(state= 'normal')
        text_sw_changes_required.insert(tk.END, outputSwChanges + '\n')
        text_sw_changes_required.tag_add("center_text",'1.0', 'end' )
        text_sw_changes_required.config(state= 'disabled')
        text_successor_notes.config(state= 'normal')
        text_successor_notes.insert(tk.END, formatNote + '\n')
        text_successor_notes.config(state= 'disabled')
    
    #final note to append
    text_successor_notes.config(state= 'normal')
    text_successor_notes.insert(tk.END, '-----------------------------------------------------\n')
    text_successor_notes.insert(tk.END, 'Please ensure successor(s) is (are) not obsolete too.')
    text_successor_notes.config(state= 'disabled')


def on_github_link_click():
    webbrowser.open_new_tab('https://github.com/ChrisHairstonBnR/Python-Successor-Finder/issues/new/choose')

#----- GUI -----#
initSettings = settings.appSettings()

# Create the main window
root = ThemedTk(theme=initSettings.defaultTheme, toplevel= True, themebg=True)
root.title("BnR SPF v%s" % sofwareVersion)

#get themes
optionTheme = tk.StringVar(value=initSettings.defaultTheme)
optionThemeList = root.get_themes()
#exclude broken themes
optionThemeList.remove('radiance')
optionThemeList.remove('ubuntu')
optionThemeList.remove('xpnative')
optionThemeList.remove('winnative')
#sort list
optionThemeList.sort() 


# Application Icon
icon = tk.PhotoImage(file= 'assets\BnR SPF Logo.png')
root.wm_iconphoto(True, icon)

# Menu Setup
menubar = tk.Menu(root)
optionMenu = tk.Menu(menubar, tearoff=0)
themeMenu = tk.Menu(optionMenu, tearoff=0)
for theme in optionThemeList:
    themeMenu.add_radiobutton(label=theme.capitalize(), variable=optionTheme, value=theme, command=selectTheme)

#Menu Variables
menuShowInputInOutput = tk.BooleanVar(value=initSettings.showInputInOutput)
menuShowInputInNotes = tk.BooleanVar(value=initSettings.showInputInNotes)

prefMenu = tk.Menu(optionMenu,tearoff=0)
prefMenu.add_cascade(label="Theme", menu=themeMenu)
prefMenu.add_checkbutton(label="Include Input In Output", variable=menuShowInputInOutput, onvalue=1, offvalue=0, command=prefChange)
prefMenu.add_checkbutton(label="Include Input In Notes", variable=menuShowInputInNotes, onvalue=1, offvalue=0, command=prefChange)
prefMenu.add_separator()
prefMenu.add_cascade(label="Reset Default Settings", command=resetDefaults)

optionMenu.add_cascade(label="Preferences", menu=prefMenu)
#optionMenu.add_separator()
optionMenu.add_command(label="About", command=openAbout)
optionMenu.add_separator()
optionMenu.add_command(label="Exit", command=closeApp)

menubar.add_cascade(label="Options", menu=optionMenu)

# Create the GUI widgets
label_obsolete_part = ttk.Label(root, text="Obsolete Part Number(s):")
entry_obsolete_part = tk.Text(root, height= 10, width= 25)
button_search = ttk.Button(root, text="Search", command=on_button_click)
label_successor_part = ttk.Label(root, text="Successor Part Number(s):")
text_successor_output = tk.Text(root, height= 10, width= 40, bg='#D3D3D3')
label_successor_notes = ttk.Label(root, text= "Notes:")
text_successor_notes = tk.Text(root, height = 10, width= 75, bg="#FFFDD0")
button_github_link = tk.Button(root, text= "To report a bug or missing material, or to request a feature or note, create an issue at https://github.com/ChrisHairstonBnR/Python-Successor-Finder/issues or click here.", command=on_github_link_click, border=0, bg=root['background'], fg=invertHexColor(root['background']))
notes_scrollbar = ttk.Scrollbar(root, orient='horizontal')
output_scrollbar = ttk.Scrollbar(root, orient='horizontal')
label_sw_changes_required = ttk.Label(root, text= "SW Changes Required?")
text_sw_changes_required = tk.Text(root, height= 10, width= 15, bg='#D3D3D3')
button_clearOutputs = ttk.Button(root, text="Clear Outputs", command=lambda: clearAll(False))
button_clearAll = ttk.Button(root, text="Clear All", command=lambda: clearAll(True))
vertical_scrollbar = ttk.Scrollbar(root, orient='vertical')

#Widget configuration
text_successor_notes.config(xscrollcommand=notes_scrollbar.set, wrap="none", state= 'disabled', yscrollcommand=syncScroll)
text_successor_output.config(xscrollcommand=output_scrollbar.set, state= 'disabled', wrap='none', yscrollcommand=syncScroll, ) #Set text boxes as read only
text_sw_changes_required.config(state='disabled', wrap='none', yscrollcommand=syncScroll)
entry_obsolete_part.config(wrap='none', yscrollcommand=syncScroll)
notes_scrollbar.config(command=text_successor_notes.xview)
output_scrollbar.config(command=text_successor_output.xview)
menubar.config(bg=root['background'], fg= invertHexColor(root['background']))
root.config(menu= menubar)
vertical_scrollbar.config(command=syncScroll)

#Grid configuration
#rows
root.rowconfigure(index=0, weight=0)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=0)
root.rowconfigure(index=3, weight=0)

#columns
root.columnconfigure(index=0, weight=0)
root.columnconfigure(index=1, weight=0)
root.columnconfigure(index=2, weight=0)
root.columnconfigure(index=3, weight=1)

# Text "tag" configuration
text_sw_changes_required.tag_configure("center_text", justify='center')


# Position the widgets using the grid geometry manager
label_obsolete_part.grid(row=0, column=0, padx=5, pady=5)
entry_obsolete_part.grid(row=1, column=0, padx=5, pady=5, sticky='ns')
button_search.grid(row=2, column=0, padx=5, pady=5)
label_successor_part.grid(row=0, column=1, padx=5, pady=5)
text_successor_output.grid(row=1, column=1, padx=5, pady=5, sticky='ns')
label_successor_notes.grid(row=0, column=3, padx=5, pady=5)
text_successor_notes.grid(row=1, column=3, padx=5, pady=5, sticky='news')
button_github_link.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='e')
notes_scrollbar.grid(row=2, column=3, sticky='ew')
output_scrollbar.grid(row=2, column=1, sticky='ew')
label_sw_changes_required.grid(row=0, column=2, padx=5, pady=5)
text_sw_changes_required.grid(row=1, column=2, padx=5, pady=5, sticky='ns')
button_clearOutputs.grid(row=3, column=0, padx=5, pady=5, sticky= 'e')
button_clearAll.grid(row=3, column=0, padx=5, pady=5, sticky= 'w')
vertical_scrollbar.grid(row=1, column=4, padx=5, pady=5, sticky='ns')

#Check for Update
u = Updater()
if not u.error:
    latestRelease = u.latestVersion[1:]
    while str(latestRelease)[-1].isalpha(): #removes characters such as 'a' or 'b' from software version
        latestRelease = latestRelease[:-1]

    sofwareVersionNum = sofwareVersion[1:]
    while str(sofwareVersionNum)[-1].isalpha(): #removes characters such as 'a' or 'b' from software version
        sofwareVersionNum = sofwareVersionNum[:-1]

    if float(sofwareVersionNum) < float(latestRelease):
        updateAvailable = True
        #updateResponse = messagebox.askokcancel('WARNING: UPDATE AVAILABLE', 'IT IS STRONGLY RECOMMENDED THAT YOU DOWNLOAD THE LATEST VERSION, %s. USING AN OUTDATED VERSION OF THIS SOFTWARE WILL LEAD TO MISINFORMATION.' % u.latestVersion)
        updateResponse = messagebox.showwarning ('WARNING: UPDATE AVAILABLE', 'IT IS STRONGLY RECOMMENDED THAT YOU DOWNLOAD THE LATEST VERSION, %s. USING AN OUTDATED VERSION OF THIS SOFTWARE WILL LEAD TO MISINFORMATION.\n\n Would you like to download the update now?' % u.latestVersion, type = 'yesno')

        if updateResponse == True or updateResponse == 'yes':
            webbrowser.open_new_tab(u.latestVersionLink)
        else:
            pass
    elif float(sofwareVersionNum) > float(latestRelease):
        hasDevVersion = True

    elif float(sofwareVersionNum) == float(latestRelease):
        hasLatestVersion = True
else:
    offlineMode = True
    root.update()
    messagebox.showwarning("Offline Mode", "The application could not connect in order to check for updates.")
    root.title("BnR SPF v%s (Offline)" % sofwareVersion)

# Start the main loop
root.mainloop()





