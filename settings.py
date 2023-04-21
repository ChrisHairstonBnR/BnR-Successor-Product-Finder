import configparser, os

config = configparser.ConfigParser()

class appSettings:

    def __init__(self):
        config.read(os.path.join(os.path.dirname(__file__), 'settings.ini'))
        #DEFAULT
        self.defaultTheme = config['DEFAULT']['DefaultTheme']

    def setDefaultTheme(self, theme):
        config['DEFAULT']['DefaultTheme'] = theme
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
        self.defaultTheme = theme