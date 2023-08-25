import configparser, os

config = configparser.ConfigParser()
appDataPath = os.getenv('LOCALAPPDATA')
settingsPath = appDataPath + '\BnR SPF\settings.ini'

class appSettings:

    def __init__(self):
        if os.path.exists(settingsPath): #If the file already exists, read the settings
           config.read(settingsPath)
        else:
            self.defaultSettings()   #if not set up defaults

        #try to pull setting but if that doesn't work (i.e. the ini file was wrongly manipulated) just set defaults
        #this should be done individually for each setting 
        #Default Theme
        try: 
            self.defaultTheme = config['DEFAULT']['DefaultTheme'] #save setting as member
        except:
            self.defaultTheme = 'default'
            config['DEFAULT'] = {'DefaultTheme' : 'default'} 
        #Show input material in output
        try:
            self.showInputInOutput = eval(config['Display']['ShowInputInOutput'].lower().capitalize()) #Shoud be "True" or "False"
        except:
            #config['Display']['ShowInputInOutput'] = 'true'
            self.showInputInOutput = True
            if config.has_section("Display"):
                config['Display']['ShowInputInOutput'] = 'true'
            else:
                config['Display'] = {'ShowInputInOutput' : 'true', 'ShowInputInNotes' : 'true'}
                
        #Show input material in notes
        try:
            self.showInputInNotes = eval(config['Display']['ShowInputInNotes'].lower().capitalize()) #Shoud be "True" or "False"
        except:
            self.showInputInNotes = True
            if config.has_section("Display"):
                config['Display']['ShowInputInNotes'] = 'true'
            else:
                config['Display'] = {'ShowInputInOutput' : 'true', 'ShowInputInNotes' : 'true'}


        self.saveSettings()
        

    def saveSettings(self):
        #Settings that don't exist in this version will be deleted
        with open(settingsPath, 'w') as configfile: 
            config.write(configfile)


    def setDefaultTheme(self, theme):
        config['DEFAULT']['DefaultTheme'] = theme #set DefaultTheme to the input parameter
        self.saveSettings()
        self.defaultTheme = theme #save member

    def restoreDefaultSettings(self):
        #Write default settings for the settings.ini file
        config['DEFAULT'] = {'DefaultTheme' : 'default'} 
        config['Display'] = {'ShowInputInOutput' : 'true'}
        config['Display'] = {'ShowInputInNotes' : 'true'}

        #Write default settings to member
        self.defaultTheme = 'default'
        self.showInputInOutput = 'true'
        self.showInputInNotes = 'true'

        os.makedirs(os.path.dirname(settingsPath), exist_ok=True) #create file if nonexistent
        self.saveSettings()