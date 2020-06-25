import socket
from Settings import HOST, PORT, NICKNAME, TOKEN, CHANNEL

def openSocket():
    sock = socket.socket()
    sock.connect((HOST, PORT))

    sock.send((f"PASS " + TOKEN + "\r\n").encode('utf-8'))
    sock.send((f"NICK " + NICKNAME + "\r\n").encode('utf-8'))
    sock.send((f"JOIN #" + CHANNEL + "\r\n").encode('utf-8'))

    return sock


def sendMessage(sock, message):

    messageTemp =  f"PRIVMSG #" + CHANNEL + " :" + message
    sock.send((messageTemp + "\r\n").encode('utf-8'))
    print("Sent: " + messageTemp)
