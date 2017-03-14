import os

count = 0
driver = open("driver", "w")
queryTypes = ["A", "AAAA", "NS", "TXT" ,"ANY"]
for zone in os.listdir("/etc/bind/zoneFiles"):
    if count % 5 == 0:
        zone = "nx"+zone
    driver.write(zone+" "+queryTypes[count % len(queryTypes)]+"\n")
    count += 1