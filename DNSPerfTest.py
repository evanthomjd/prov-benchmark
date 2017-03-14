import subprocess
import threading
import socket
import logging

runPerf = False
count = 0
logFile = "/var/log/oarc/dnsPerfTest"

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO, filename="/var/log/oarc/perfTest.log")

def perfTest():
    while runPerf:
        perResults = open((logFile+"_%s") % count, "a")
        perf = subprocess.Popen(["dnsperf", "-n", "25", "-d", "/media/sf_shared-vb/OARC-Research/driver", "-Q", "1000"],
                                stdout=perResults, stderr=perResults)
        perf.communicate()
        perResults.close()


def handleMessage(message):
    noX = message.replace("X", "")
    if len(noX) > 0:
        return noX
    else:
        return message



server = socket.socket()
host = socket.gethostname()
print host
port = 12345
client = None
try:
    server.bind((host, port))
    server.listen(5)
    client, clientAddr = server.accept()
    message = handleMessage(client.recv(1024))
    print "START ", message
    while len(message) != 0:
        print message
        if message == "START":
            logging.info("Starting DNS Perf Test")
            runPerf = True
            perfThread = threading.Thread(target=perfTest, args=[])
            perfThread.start()
            client.send("STARTED")
        elif message == "STOP":
            logging.info("Stopping DNS Perf Test")
            runPerf = False
            perfThread.join()
            logging.info("DNS Perf Test Stopped")
            client.send("STOPPED")
        elif message == "ROLL":
            count += 1
            client.send("ROLLED")
        else:
            logging.info("Unkown message recieved %s", message)
        message = handleMessage(client.recv(1024))


    logging.info("All testing complete, shutting down")
    client.close()
    server.close()

except Exception, e:
    logging.error("Exception!", exec_info=True)
finally:
    if client != None:
        client.close()
    server.close()
