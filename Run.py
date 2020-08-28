from Socket import openSocket, sendMessage, sendWhisper, initChannels
from Initialize import *
from Read import *
import time
from Settings import *
import random

if LANGUAGE == "en":
    from Textsen import *
else:
    from Textstr import *

sock = openSocket()
joinRoom(sock)

readBuffer = ""

selamcooldown = {}  # Cooldown dict for 'selam' command
selamMetinleri = ('selam', 'sa', 'hello', 'hi', 'hey', 'merhaba', 'selamlar', 'merhabalar')
lastchatters = {"silveraxe":99999999999999,"moobot":999999999999999}
lastheyo = 0
hflast={}
grwords=["Harikasın", "Muhteşemsin", "Süpersin"]
reactiontimer = 0
wordslist="abcdefghijklmnoprstuvyzqwxABCDEFGHIJKLMNOPRSTUVYZQWX123456789"
reactionOn=False
code="This is a sample code to dont let them know thisS"


while True:

    '''Date = (datetime.datetime.today().utcnow() + datetime.timedelta(hours=GMT)) # notify eklenecek
    if notifyWeekly(Date, 2, 15, 54):
        sendMessage(sock, 'deltaoxide', 'Saat 13:20')'''

    readBuffer = readBuffer + sock.recv(2048).decode('utf-8')
    temp = readBuffer.split('\n')
    readBuffer = temp.pop()


    #                                    ------- Notifications --------
    # -------------------------------------------------------------------------------------------------------------



    for line in temp:
        print(line)
        if line.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
            break

        msgType = getMsgType(line)
        message = getMessage(line).replace("\r","")
        channel = getChannel(line)
        user = getUser(line)
        arguments = message.split(" ")
        content = (" ".join((message.split(" "))[1::]))
        msgType = getMsgType(line)

#                                         ------    Komutlar    ------
# -----------------------------------------------------------------------------------------------------------------

        # ------ Selam Verme

        '''if stringFormat(arguments[0].lower()) in selamMetinleri or message.lower().startswith("iyi yayınlar"):
            if user not in selamcooldown or time.time() - selamcooldown[user] > 14400:
                if msgType == "PRIVMSG":
                    sendMessage(sock,channel, MSG_HELLO + user + " VoHiYo")
                    selamcooldown[user] = time.time()'''

        if "@deltaoxidebot" in message.lower():
            if messageCooldown("dbottagged",300):
                sendMessage(sock, channel,f"Merhaba {user}. Benimle konuşmaya çalıştığını anlıyorum fakat ben sadece sahibimin eğittiği bir robot kediyim ve seni anlayamam VoHiYo")

        if channel == 'oykeli':
            '''if time.time() - lastheyo > 600 :
                if msgType == "PRIVMSG":
                    sendMessage(sock, channel,"VoHiYo")
                    lastheyo = time.time()'''

            if arguments[0].lower() == "?highfive":
                try:
                    target = arguments[1].replace("@", "").lower()
                except IndexError:
                    break
                if user.lower() in hflast and time.time() - hflast[user.lower()] < 50:
                    sendMessage(sock, channel,target + " > GivePLZ TakeNRG < " + user)
                elif target not in hflast:
                    hflast[target] = time.time()

            if arguments[0].lower() == "?öv":
                try:
                    target = arguments[1].replace("@", "").lower()
                except IndexError:
                    target = user
                gr = grwords[random.randint(0, len(grwords)-1)]
                sendMessage(sock, channel,gr + " " + target + " BloodTrail")

            if time.time() - reactiontimer > 3600:
                code=""
                while len(code)<4:
                    code = code + f"{wordslist[random.randint(0,len(wordslist)-1)]}"
                print(code)
                sendMessage(sock, channel,"[ReaksiyonTesti] Kodu chate ilk yazan kazanır : " + code + " PogChamp")
                reactiontimer = time.time()
                reactionOn = True
            if reactionOn and message == code:
                sendMessage(sock, channel, "[ReaksiyonTesti] Tebrikler @" + user + " Kazandın BloodTrail")
                reactionOn=False

        if channel == 'silveraxe':
            if user not in lastchatters or time.time() - lastchatters[user] > 18000 :
                if msgType == "PRIVMSG":
                    sendMessage(sock, channel, MSG_HELLO + user + " VoHiYo")
                    lastchatters[user] = time.time()

        # -------- Channel Silveraxe
        if channel == 'silveraxe':
            if arguments[0].lower() in ['!şarkı', '!song']:
                sendMessage(sock, channel, MSG_SONG + '\r' + getSong())

            if arguments[0].lower() == ("!artchallenge"):
                if messageCooldown("!artchallenge", 300):
                    sendMessage(sock,channel, MSG_ARTCH)

        # --------------------------- Deltaoxide

        if message.startswith("ping") and user == "deltaoxide":
            sendMessage(sock,channel, "pong")

        if message.startswith('?language') and user == "deltaoxide":
            if LANGUAGE == 'en':
                from Textstr import *
                sendMessage(sock, channel, 'Dil \'Türkçe\' olarak ayarlandı')
            else:
                from Textsen import *
                sendMessage(sock, channel, 'Language has been set as \'English\'')

        # ----------- Dashboard
        if channel == 'deltaoxide':
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
                        sendMessage(sock,"deltaoxide","Ayrılmak istediğiniz kişi #" + arguments[1] + " takipten çıkarılamadı.")
                else:
                    sendMessage(sock,"deltaoxide", "Eklemeye çalıştığınız kişi #" + arguments[1] + " zaten listede")

        # ----------------------------------------- Time dependent auto exect functions --------------------------

        '''if messageCooldown('salı',43200):
            if getDate()['weekday'] == 2:
                getDate()['hours']
            else:
                messageCooldown('salı', 43200)'''



