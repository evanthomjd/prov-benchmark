import random
from ZoneGenerator import ZoneGenerator
from dnsUtil import BindUtil
import sys


def writeZoneFiles(number_of_files, number_of_records, generator):
    for count in range(0, number_of_files):
        if count % 2 == 0:
            if random.random() > 0.5:
                generator.writeZoneFile(number_of_records + 100, generator.generateZoneName())
            else:
                generator.writeZoneFile(max(0, number_of_records - 100), generator.generateZoneName())
        else:
            generator.writeZoneFile(number_of_records, generator.generateZoneName())




assert len(sys.argv) == 5, "Please enter include file location, zone file location, Name Server Software, dynamic"

includeLoc = sys.argv[1]
zoneFileLoc = sys.argv[2]
ns = sys.argv[3]
dynamic = bool(int(sys.argv[4]))

# wordBank = ['meredith', 'dilara', 'nunney', 'slaughter', 'montreal', 'degrasee', 'itertools', 'upthecuts','humidifier', 'pipeline']
wordBank = ['degrassee', 'itertools']

if ns == "BIND":
    masterUtil = BindUtil.BindUtil("/etc/bind/include.inc", "/etc/bind/zoneFiles", "master")



masterUtil.cleanFiles()
generator = ZoneGenerator(wordBank, masterUtil, dynamic)


print "Writing Min size Zones"
writeZoneFiles(100, 5, generator)
print "Finished Writing Min size Zones"


print "Writing Max size Zones"
writeZoneFiles(100, 1000, generator)
print "Finished Writing Max Size"

print "Writing Average size Zones"
writeZoneFiles(100, 10, generator)
print "Finished Writing Average size Zones"


if not dynamic:
    print "Reconfig Start"
    masterUtil.reconfig()
    print "Reconfig Finished"
