import time
from Socket import sendMessage, initChannels
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

    sock.send((f"CAP REQ :twitch.tv/commands\r\n").encode('utf-8'))
    for chan in initChannels:
        sendMessage(sock,chan,MSG_FIRST)


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