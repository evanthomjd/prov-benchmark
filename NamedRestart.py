import socket
import os
import logging


def handleMessage(message):
    noX = message.replace("X", "")
    if len(noX) > 0:
        return noX
    else:
        return message


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO, filename="/var/log/oarc/namedRestart.log")

server = socket.socket()
host = socket.gethostname()
port = 12346
client = None

try:
    os.system("service bind9 restart")
    server.bind((host, port))
    server.listen(5)


    client, clientAddr = server.accept()

    message = handleMessage(client.recv(1024))
    print "START ", message
    while len(message) != 0:
        print message
        if message == "RESTART":
            logging.info("Recieved signal to restart bind")
            os.system("service bind9 restart")
            logging.info("Restart Complete")
            client.send("DONE")
        message = handleMessage(client.recv(1024))

except Exception, e:
    logging.error("Exception!", exec_info=True)
finally:
    if client != None:
        client.close()
    server.close()

