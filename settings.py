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

        #DEFAULT
        self.defaultTheme = config['DEFAULT']['DefaultTheme'] #save setting as member

    def setDefaultTheme(self, theme):
        config['DEFAULT']['DefaultTheme'] = theme #set DefaultTheme to the input parameter
        with open(settingsPath, 'w') as configfile: #write to file
            config.write(configfile)
        self.defaultTheme = theme #save member

    def defaultSettings(self):
        #Write default settings for the settings.ini file
        config['DEFAULT'] = {'DefaultTheme' : 'default'}
        os.makedirs(os.path.dirname(settingsPath), exist_ok=True)
        with open(settingsPath, 'w') as configfile:
            config.write(configfile)