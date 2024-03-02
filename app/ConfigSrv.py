import configparser

class ConfigSrv:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('app.ini')
    
    def updateParam(self, key, value):
        self.config['PARAMS'][key] = value
        self.__updateConfigFile()
    
    def getValue(self, key):
        return self.config['PARAMS'][key]

    def listParams(self):
        return self.config['PARAMS']
    
    def __updateConfigFile(self):
        with open('app.ini', 'w') as configfile:
            self.config.write(configfile)
    

if __name__ == '__main__':


    srv = ConfigSrv()
    srv.updateParam('SURFACE_DEPTH', "-1")
    list = srv.listParams()
    for key in list:
        print("%s:%s" % (key, list[key]))



