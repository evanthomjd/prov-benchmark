from DNSSoftwareUtil import DNSSoftwareUtil
import os
import time
import shutil


class BindUtil(DNSSoftwareUtil):
    MASTER_INC_STATEMENT = """"%s" { type master; allow-transfer {127.0.0.1;}; file "%s/%s";};"""

    SLAVE_INC_STATEMENT = """"%s" {type slave; masters { 127.0.0.1; }; allow-transfer {127.0.0.1;}; file "%s/%s";};"""


    def __init__(self, configLocation, zoneFileLocation, type):
        DNSSoftwareUtil.__init__(self, configLocation, zoneFileLocation)
        if type == 'slave':
            self.include = self.SLAVE_INC_STATEMENT
        else:
            self.include = self.MASTER_INC_STATEMENT


    def writeZoneConfig(self, zoneName):
        configFile = file(self.configLocation, 'a')
        configFile.write(("zone "+self.include+"\n") %(zoneName, self.zoneFileLocation, zoneName))
        self.logZone(zoneName)
        configFile.close()

    def reconfig(self):
        start = time.time()
        os.system("rndc reconfig")
        return time.time() - start;


    def dynamicZoneAdd(self, zoneName):
        start = time.time()
        os.system(("rndc addZone '"+self.include+"'") % (zoneName, self.zoneFileLocation, zoneName))
        finish = time.time()
        self.logZone(zoneName)
        return finish - start


    def cleanFiles(self):
        os.system("service bind9 stop")
        configFile = file(self.configLocation, 'rw+')
        configFile.truncate()
        configFile.close()
        shutil.rmtree(self.zoneFileLocation)
        os.mkdir(self.zoneFileLocation)
        if os.path.isfile("/var/cache/bind/3bf305731dd26307.nzf"):
            os.remove("/var/cache/bind/3bf305731dd26307.nzf")
        os.system("service bind9 start")

    def restart(self):
        os.system("service bind9 restart")





