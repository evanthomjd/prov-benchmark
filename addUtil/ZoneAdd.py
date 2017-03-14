import time
import logging

class ZoneAdd():

    def __init__(self, dnsUtil, zoneList, isDynamic, batchSize):
        self.dnsUtil = dnsUtil
        self.zoneList = zoneList
        self.isDynamic = isDynamic
        self.batchSize = batchSize
        self.addTime = 0.0
        self.reconfigs = 0.0
        self.averageCallTime = 0.0
        self.logger = logging.getLogger()

    def run(self):
        self.addZones()

        if not self.isDynamic:
            self.logger.info("Starting reconfig")
            self.addTime += self.dnsUtil.reconfig()
            self.logger.info("Ending reconfig")
            self.reconfigs += 1.0

        if self.isDynamic:
            self.averageCallTime = self.addTime/float(len(self.zoneList))
        else:
            self.averageCallTime = self.addTime / self.reconfigs

    def reset(self):
        self.addTime = 0.0
        self.reconfigs = 0.0
        self.averageCallTime = 0.0
        self.dnsUtil.cleanFiles()
        self.dnsUtil.restart()


    def addZones(self):
        with open(self.zoneList) as zones:
            for count, zone in enumerate(zones):
                zone = zone.replace("\n", "")
                self.addZone(zone)
                if (count+1) % self.batchSize == 0:
                    if not self.isDynamic:
                        self.logger.info("Starting reconfig")
                        self.addTime += self.dnsUtil.reconfig()
                        self.logger.info("Ending reconfig")
                        self.reconfigs += 1.0
                    else:
                        time.sleep(30)
                    self.logger.info("Batch added, isDyamic=[%s]", self.isDynamic)


    def addZone(self, zone):
        if self.isDynamic:
            self.addTime += self.dnsUtil.dynamicZoneAdd(zone)
        else:
            self.dnsUtil.writeZoneConfig(zone)
