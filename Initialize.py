import time
from Socket import sendMessage
from Settings import LANGUAGE

if LANGUAGE == "en":
    from Textsen import MSG_FIRST
else:
    from Textstr import MSG_FIRST

commandcoold={}
def joinRoom(sock):
    readBuffer = ""
    Loading = True

    while Loading:
        readBuffer = readBuffer + sock.recv(2048).decode('utf-8')
        temp = readBuffer.split('\n')
        readBuffer = temp.pop()

        for line in temp:
            print(line)
            Loading = loadingComplete(line)

    sendMessage(sock,MSG_FIRST)

def say(msg):
    sendMessage(sock, msg)

def messageCooldown(command,duration):
    if command not in commandcoold or time.time() - commandcoold[command] > duration :
        commandcoold[command]= time.time()
        return True
    else:
        return False


def loadingComplete(line):
    if "End of /NAMES list" in line:
        return False
    else:
        return True