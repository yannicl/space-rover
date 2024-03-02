import ujson

class ConfigSrv:
    def __init__(self):
        with open('config.json', "r") as fp:
            self.params = ujson.load(fp)

    def updateParam(self, key, value):
        self.params[key] = value
        self.__updateConfigFile()
    
    def getValue(self, key):
        return self.params[key]
    
    def listParams(self):
        return self.params

    def __updateConfigFile(self):
        with open('config.json', "w") as fp:
            ujson.dump(self.params, fp)

if __name__ == '__main__':

    srv = ConfigSrv()
    srv.updateParam('SURFACE_DEPTH', "-1")
    list = srv.listParams()
    for key in list:
        print("%s:%s" % (key, list[key]))