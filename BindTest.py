from addUtil import ZoneAdd
from dnsUtil import BindUtil
import logging
import sys
import socket
import time
import threading
import os

def sendAndWait(sender, message):
    sender.send(message)
    sender.recv(1024)


def keepAlive():
    while running:
        perfServer.send("X")
        masterServer.send("X")
        time.sleep(5)

def zoneFileCount(path):
    start = time.time()
    count = [zone for zone in os.listdir(path) if not zone.endswith(".jnl")]
    while count != 10000:
        time.sleep(5)
        count = [zone for zone in os.listdir(path) if not zone.endswith(".jnl")]
    end = time.time()
    logging.info("[ALL Zone Files] time=[%s]", end-start)

assert len(sys.argv)==7, "Pass in numberOfTests, isDynamic, dnsPerf host, dnsPerf port, masterNS host, mastNS port"
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO, filename="/var/log/oarc/configTest.log")

running = False
numberOfTests = int(sys.argv[1])
dynamic = bool(int(sys.argv[2]))
perfHost = sys.argv[3]
perfPort = int(sys.argv[4])
masterHost = sys.argv[5]
masterPort = int(sys.argv[6])
perfServer = None
masterServer = None

batchSizes = [100, 150]

try:
    perfServer = socket.socket()
    perfServer.connect((perfHost, perfPort))

    masterServer = socket.socket()
    masterServer.connect((masterHost, masterPort))

    slaveUtil = BindUtil.BindUtil("/etc/bind/slaveInclude.inc", "/etc/bind/slaveZones", "slave")

    callTimeSum = 0.0

    ka = threading.Thread(target=keepAlive, args=[])
    running = True
    ka.start()
    for batchSize in batchSizes:
        addZone = ZoneAdd.ZoneAdd(slaveUtil, "/var/log/oarc/zones_1488658347.log", dynamic, batchSize)
        slaveUtil.cleanFiles()
        logging.info("[Tests Start] batch_size=[%s], isDynamic=[%s]", batchSize, dynamic)
        for count in range(0, numberOfTests):
            fileCount = threading.Thread(target=zoneFileCount, args=[slaveUtil.zoneFileLocation])
            fileCount.start()
            logging.info("##########################")
            logging.info("[Test Start] batchSize=[%s], run_through=[%s]", batchSize, count)
            sendAndWait(perfServer, "START")
            addZone.run()
            sendAndWait(perfServer, "STOP")
            logging.info("[Test Complete] batchSize=[%s], run_through=[%s], average_call_time=[%s]", batchSize, count, addZone.averageCallTime)
            logging.info("##########################")
            callTimeSum += addZone.averageCallTime
            logging.info("Reset")
            fileCount.join()
            addZone.reset()
            sendAndWait(masterServer, "RESTART")
            logging.info("Reset Complete")

        averageCallTime = callTimeSum / float(numberOfTests)
        logging.info("[Tests Complete] batch_size=[%s], isDynamic=[%s], average_call_time=[%s]", batchSize, dynamic,
                     averageCallTime)
        sendAndWait(perfServer, "ROLL")

    running = False
    ka.join()

except Exception, e:
    logging.error(exec_info=True)

finally:
    if perfServer != None:
        perfServer.close()
    if masterServer != None:
        perfServer.close()