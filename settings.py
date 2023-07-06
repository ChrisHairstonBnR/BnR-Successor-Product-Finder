import configparser, os

config = configparser.ConfigParser()
appDataPath = os.getenv('LOCALAPPDATA')
settingsPath = appDataPath + '\BnR SPF\settings.ini'

class appSettings:

    def __init__(self):
        if os.path.exists(settingsPath):
           config.read(settingsPath)
        else:
            self.defaultSettings()   

        #DEFAULT
        self.defaultTheme = config['DEFAULT']['DefaultTheme']

    def setDefaultTheme(self, theme):
        config['DEFAULT']['DefaultTheme'] = theme
        with open(settingsPath, 'w') as configfile:
            config.write(configfile)
        self.defaultTheme = theme

    def defaultSettings(self):
        config['DEFAULT'] = {'DefaultTheme' : 'default'}
        os.makedirs(os.path.dirname(settingsPath), exist_ok=True)
        with open(settingsPath, 'w') as configfile:
            config.write(configfile)