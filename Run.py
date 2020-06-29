from Socket import openSocket, sendMessage, sendWhisper, initChannels
from Initialize import *
from Read import *
import time
from Settings import *

if LANGUAGE == "en":
    from Textsen import *
else:
    from Textstr import *

sock = openSocket()
joinRoom(sock)

readBuffer = ""

selamcooldown = {}  # Cooldown dict for 'selam' command

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
# -----------------------------------------------------------------------------------------------------------------

        # ------ Selam Verme
        if arguments[0].lower() in ('selam', 'sa', 'hello', 'hi', 'hey', 'merhaba', 'selamlar') or message.lower().startswith("iyi yayınlar"):
            if user not in selamcooldown or time.time() - selamcooldown[user] > 600:
                if msgType == "PRIVMSG":
                    sendMessage(sock,channel, MSG_HELLO + user + " VoHiYo")
                elif msgType == "WHISPER":
                    sendWhisper(sock,user,MSG_HELLO + user + " VoHiYo")
                selamcooldown[user] = time.time()

        if arguments[0].lower() in ['!şarkı', '!song'] and user == 'deltaoxide':
            sendMessage(sock, channel, MSG_SONG + '\r' + getSong())

        # ------ Art Challenge Bilgi
        if message.lower().startswith("?artchallenge") and messageCooldown("?artchallenge", 300):
            sendMessage(sock,channel, MSG_ARTCH)

            # --------------------------------------------------------------------------------------------------

        if message.startswith("ping") and user == "deltaoxide":
            sendMessage(sock,channel, "pong")

        if message.startswith('?language') and user == "deltaoxide":
            if LANGUAGE == 'en':
                from Textstr import *
                sendMessage(sock, channel, 'Dil \'Türkçe\' olarak ayarlandı')
            else:
                from Textsen import *
                sendMessage(sock, channel, 'Language has been set as \'English\'')

        if message.startswith("?katıl") and user == "deltaoxide":
            if arguments[1] not in initChannels:
                '''Follow the channel and if true join the channel'''
                if followChan(arguments[1]):
                    initChannels.append(arguments[1])
                    chanfile=open("channels.txt","w")
                    chanfile.write(("\n".join(initChannels)))
                    chanfile.close()
                    sock.send((f"JOIN #" + arguments[1] + "\r\n").encode('utf-8'))
                    sendMessage(sock,arguments[1] , MSG_FIRST)
                    sendMessage(sock, "deltaoxide", "Bu kanala katıldık : #" + arguments[1])
                else:
                    sendMessage(sock, "deltaoxide", "Eklemeye çalıştığınız kişi #" + arguments[1] + " takip edilemedi.")
            else:
                sendMessage(sock,"deltaoxide", "Eklemeye çalıştığınız kişi #" + arguments[1] + " zaten listede")

        if message.startswith("?ayrıl") and user == "deltaoxide":
            if arguments[1] in initChannels:
                if unfChan(arguments[1]):
                    initChannels.remove(arguments[1])
                    chanfile=open("channels.txt","w")
                    chanfile.write(("\n".join(initChannels)))
                    chanfile.close()
                    sock.send((f"PART #" + arguments[1] + "\r\n").encode('utf-8'))
                    sendMessage(sock, "deltaoxide", "Bu kanaldan ayrıldık : #" + arguments[1])
                else:
                    sendMessage(sock,"deltaoxide","Eklemeye çalıştığınız kişi #"+arguments[1]+" takipten çıkarılamadı.")
            else:
                sendMessage(sock,"deltaoxide", "Eklemeye çalıştığınız kişi #" + arguments[1] + " zaten listede")


