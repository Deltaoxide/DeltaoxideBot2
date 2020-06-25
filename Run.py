from Socket import openSocket, sendMessage
from Initialize import joinRoom,messageCooldown
from Read import getMessage, getUser
import time

from Settings import LANGUAGE

if LANGUAGE == "en":
    from Textsen import MSG_ARTCH, MSG_HELLO
else:
    from Textstr import MSG_ARTCH, MSG_HELLO

sock = openSocket()
joinRoom(sock)

readBuffer = ""
selamcooldown={}

while True:
    readBuffer = readBuffer + sock.recv(2048).decode('utf-8')
    temp = readBuffer.split('\n')
    readBuffer = temp.pop()
    for line in temp:
        print(line)
        if line.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
            break

        user = getUser(line)
        message = getMessage(line)
        print (user + " typed :" + message)
        #commands ...


        #MSG_HELLO
        if "selam" in message or "merhaba" in message or "sa" in message or "hello" in message  :
            if user not in selamcooldown or time.time() - selamcooldown[user] > 600 :
                sendMessage(sock, MSG_HELLO +user+" VoHiYo")
                selamcooldown[user]=time.time()


        #MSG_ARTCH
        if message.startswith("?artchallenge") and messageCooldown("?artchallenge",300) :
            sendMessage(sock, MSG_ARTCH)
