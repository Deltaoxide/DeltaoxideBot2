import socket
from Settings import HOST, PORT, NICKNAME, TOKEN

chanfile = open("channels.txt","r")

initChannels = chanfile.read().split("\n")
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
    messagetemp = "PRIVMSG #deltaoxide :/w " + user + " "+ message
    sock.send((messagetemp + "\r\n").encode('utf-8'))
    print("Whıspered: " + messagetemp)


def sendMessage(sock,channel, message):
    messagetemp = "PRIVMSG #" + channel + " :" + message
    sock.send((messagetemp + "\r\n").encode('utf-8'))
    print("Sent: " + messagetemp)