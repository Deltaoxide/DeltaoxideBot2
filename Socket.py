import socket
from Settings import HOST, PORT, NICKNAME, TOKEN, CHANNEL

chanfile=open("channels.txt","r")
initChannels= chanfile.read().split("\n")
chanfile.close()


def openSocket():
    sock = socket.socket()
    sock.connect((HOST, PORT))

    sock.send((f"PASS " + TOKEN + "\r\n").encode('utf-8'))
    sock.send((f"NICK " + NICKNAME + "\r\n").encode('utf-8'))
    for chan in initChannels:
        sock.send((f"JOIN #" + chan + "\r\n").encode('utf-8'))



    return sock

def sendWhisper(sock,user, message):

    messageTemp =  f"PRIVMSG #deltaoxide" " :/w "+ user +" "+ message
    sock.send((messageTemp + "\r\n").encode('utf-8'))
    print("Whıspered: " + messageTemp)

def sendMessage(sock,channel, message):

    messageTemp =  f"PRIVMSG #" + channel + " :" + message
    sock.send((messageTemp + "\r\n").encode('utf-8'))
    print("Sent: " + messageTemp)