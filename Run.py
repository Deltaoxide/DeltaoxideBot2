from Socket import openSocket, sendMessage, sendWhisper, initChannels
from Initialize import joinRoom, messageCooldown
from Read import getMessage, getUser, getChannel, getMsgType
import time

from Settings import LANGUAGE

if LANGUAGE == "en":
    from Textsen import MSG_ARTCH, MSG_HELLO, MSG_FIRST
else:
    from Textstr import MSG_ARTCH, MSG_HELLO, MSG_FIRST

sock = openSocket()
joinRoom(sock)

readBuffer = ""
selamcooldown = {}

while True:
    readBuffer = readBuffer + sock.recv(2048).decode('utf-8')
    temp = readBuffer.split('\n')
    readBuffer = temp.pop()
    for line in temp:
        print(line)
        if line.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
            break

        message = getMessage(line).replace("\r","")
        channel = getChannel(line)
        user = getUser(line)
        arguments = message.split(" ")
        content = (" ".join((message.split(" "))[1::]))
        msgType = getMsgType(line)

#                                         ------    Komutlar    ------
#----------------------------------------------------------------------------------------------------------------------

        # ------ Selam Verme
        if message.startswith("selam") or message.startswith("iyi yayınlar") or arguments[0] == "sa" or arguments[0] == "hello" or arguments[0] == "hi" :
            if user not in selamcooldown or time.time() - selamcooldown[user] > 600:
                if msgType == "PRIVMSG":
                    sendMessage(sock,channel, MSG_HELLO + user + " VoHiYo")
                elif msgType == "WHISPER":
                    sendWhisper(sock,user,MSG_HELLO + user + " VoHiYo")
                selamcooldown[user] = time.time()

        # ------ Art Challenge Bilgi
        if message.startswith("?artchallenge") and messageCooldown("?artchallenge", 300):
            sendMessage(sock,channel, MSG_ARTCH)

#----------------------------------------------------------------------------------------------------------------------



        if message.startswith("ping") and user == "deltaoxide":
            sendMessage(sock,channel, "pong")

        if message.startswith("?katıl") and user == "deltaoxide":
            if arguments[1] not in initChannels:
                initChannels.append(arguments[1])
                chanfile=open("channels.txt","w")
                chanfile.write(("\n".join(initChannels)))
                chanfile.close()
                sock.send((f"JOIN #" + arguments[1] + "\r\n").encode('utf-8'))
                sendMessage(sock,arguments[1] , MSG_FIRST)
                sendMessage(sock, "deltaoxide", "Bu kanala katıldık : #" + arguments[1])

            else:
                sendMessage(sock,"deltaoxide", "Eklemeye çalıştığınız kişi #" + arguments[1] + " zaten listede")

        if message.startswith("?ayrıl") and user == "deltaoxide":
            if arguments[1] in initChannels:
                initChannels.remove(arguments[1])
                chanfile=open("channels.txt","w")
                chanfile.write(("\n".join(initChannels)))
                chanfile.close()
                sock.send((f"PART #" + arguments[1] + "\r\n").encode('utf-8'))
                sendMessage(sock, "deltaoxide", "Bu kanaldan ayrıldık : #" + arguments[1])

            else:
                sendMessage(sock,"deltaoxide", "Eklemeye çalıştığınız kişi #" + arguments[1] + " zaten listede")


