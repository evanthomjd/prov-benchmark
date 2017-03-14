from abc import ABCMeta, abstractmethod
import time

class DNSSoftwareUtil:

    __metaclass__ = ABCMeta

    zoneFileLocation = ""
    configLocation = ""
    logFile = ""


    def __init__(self, configLocation, zoneFileLocation):
        self.zoneFileLocation = zoneFileLocation
        self.configLocation = configLocation
        self.logFile = "/var/log/oarc/zones_%s.log" % (int(time.time()))

    @abstractmethod
    def writeZoneConfig(self, zoneName): pass

    @abstractmethod
    def reconfig(self): pass

    @abstractmethod
    def dynamicZoneAdd(self, zoneName): pass

    @abstractmethod
    def restart(self): pass

    @abstractmethod
    def cleanFiles(self): pass

    def writeZoneFile(self, zoneName, content):
        zoneFile = open(self.zoneFileLocation+"/"+zoneName, 'w')
        zoneFile.write(content+"\n")
        zoneFile.close()


    def logZone(self, zoneName):
        logFile = open(self.logFile, 'a')
        logFile.write(zoneName+"\n")
        logFile.close


    def swapLogFile(self):
        self.logFile = "/var/log/oarc/zones_%s.log" % (int(time.time()))