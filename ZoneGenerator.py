from itertools import permutations
import time

class ZoneGenerator:

    FILE_CONTENT = """%s IN SOA ns.admin.ca hostmaster.zone.ca 200308080	172800 900 1209600 36000
%s IN A 123.12.1.1
%s IN NS ns.%s
ns.%s IN A 8.8.8.8"""

    tlds = [".ca.", ".nz.", ".beer.", ".xxx.", ".com.", ".net.", ".kiwi.", ".se.", ".nu.", ".biz."]

    def __init__ (self, baseWords, dnsUtil, dynamic):
        self.names = set()
        self.dnsUtil = dnsUtil
        self.dynamic = dynamic
        for word in baseWords:
            self.names = self.names | set(([''.join(p) for p in permutations(word)]))

    def generateZoneName(self):
        if len(self.names) != 0:
            return self.names.pop() + self.tlds[len(self.names)%len(self.tlds)]


    def writeZoneFile(self, number_of_records, zone):
        fileContent = self.FILE_CONTENT % (zone, zone, zone, zone, zone)

        ts = int(round(time.time()))
        for rec in range(0, number_of_records):
            if rec % 3 == 0:
                newRec = "\nns%s.%s IN NS %sns.%s" % (ts, zone, rec, zone)
                newRec = newRec + "\n%sns.%s IN A 123.12.1.1" % (rec, zone)
            elif rec % 3 == 1:
                newRec = "\nns%s.%s IN NS %sns.%s" % (ts, zone, rec, zone)
                newRec = newRec + "\n%sns.%s IN AAAA 2001:500:80:2::12 " % (rec, zone)
            else:
                newRec = "\nns%s.%s IN TXT \"text record for %s\" " % (ts, zone, zone)
            fileContent = fileContent + newRec

        self.dnsUtil.writeZoneFile(zone, fileContent)
        if self.dynamic:
            self.dnsUtil.dynamicZoneAdd(zone)
        else:
            self.dnsUtil.writeZoneConfig(zone)