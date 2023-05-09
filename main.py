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
sofwareVersion = '0.8b'
updateAvailable = False
offlineMode = False
hasLatestVersion = False
hasDevVersion = False


def selectTheme():
    root.set_theme(theme_name=optionTheme.get(), themebg= True, toplevel= True)
    button_github_link.config(bg= root['background'], fg= invertHexColor(root['background']))
    initSettings.setDefaultTheme(optionTheme.get())

def closeApp():
    root.quit()



def openAbout():

    def closeAbout():
        child_about.destroy()
    
    def clickUpdate():
        webbrowser.open_new_tab(u.latestVersionLink)


    child_about = tk.Toplevel(root)
    child_about.title("About BnR SPF")
    child_about.grab_set()
    if hasLatestVersion:
        aboutTextTop = "BnR SPF\nVersion: %s (Latest)\n" % sofwareVersion
    elif hasDevVersion:
        aboutTextTop = "BnR SPF\nVersion: %s (Developement)\n" % sofwareVersion
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
        if materialOutput == 'N/A' and (lookupResult.nonDirectMsg == '' or lookupResult.nonDirectMsg == None) :
            outputSwChanges = '%s: N/A' % materialInput
        elif lookupResult.nonDirectMsg != '' and lookupResult.nonDirectMsg != None:
            outputSwChanges = '%s: yes' % materialInput
        elif lookupResult.swChangesRequired:
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
    webbrowser.open_new_tab('https://github.com/ChrisHairstonBnR/Python-Successor-Finder/issues/new/choose')

#----- GUI -----#
initSettings = settings.appSettings()

# Create the main window
root = ThemedTk(theme=initSettings.defaultTheme, toplevel= True, themebg=True)
root.title("BnR SPF v%s" % sofwareVersion)



#get and sort themes
optionTheme = tk.StringVar(value=initSettings.defaultTheme)
optionThemeList = root.get_themes()
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

optionMenu.add_cascade(label="Theme", menu=themeMenu)
optionMenu.add_command(label="About", command=openAbout)
optionMenu.add_separator()
optionMenu.add_command(label="Exit", command=closeApp)


menubar.add_cascade(label="Options", menu=optionMenu)


# Create the GUI widgets
label_obsolete_part = ttk.Label(root, text="Obsolete Part Number(s):")
entry_obsolete_part = tk.Text(root, height= 10, width= 20)
button_search = ttk.Button(root, text="Search", command=on_button_click)
label_successor_part = ttk.Label(root, text="Successor Part Number(s):")
text_successor_output = tk.Text(root, height= 10, width= 40, bg='#D3D3D3')
label_successor_notes = ttk.Label(root, text= "Notes:")
text_successor_notes = tk.Text(root, height = 10, width= 50, bg="#FFFDD0")
button_github_link = tk.Button(root, text= "To report an issue or missing material, create an issue at https://github.com/ChrisHairstonBnR/Python-Successor-Finder/issues or click here.", command=on_github_link_click, border=0, bg=root['background'], fg=invertHexColor(root['background']))
notes_scrollbar = ttk.Scrollbar(root, orient='horizontal')
output_scrollbar = ttk.Scrollbar(root, orient='horizontal')
label_sw_changes_required = ttk.Label(root, text= "Software Changes Required?")
text_sw_changes_required = tk.Text(root, height= 10, width= 25, bg='#D3D3D3')


#Widget configuration
text_successor_notes.config(xscrollcommand=notes_scrollbar.set, wrap="none", state= 'disabled')
text_successor_output.config(xscrollcommand=output_scrollbar.set, state= 'disabled', wrap='none') #Set text boxes as read only
text_sw_changes_required.config(state='disabled', wrap='none')
entry_obsolete_part.config(wrap='none')
notes_scrollbar.config(command=text_successor_notes.xview)
output_scrollbar.config(command=text_successor_output.xview)
button_github_link.config()
menubar.config(bg=root['background'], fg= invertHexColor(root['background']))
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





