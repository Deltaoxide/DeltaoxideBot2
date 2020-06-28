def getUser(line):
	try:
		separate = line.split(":", 2)
		user = separate[1].split("!", 1)[0]
		return user
	except IndexError:
		return "nulluser"


def getMessage(line):
	try:
		separate = line.split(":", 2)
		message = separate[2]
		return message
	except IndexError:
		return "nullmsg"


def getChannel(line):
	try:
		separate = line.split(" ")
		msgchannel = separate[2].replace("#","")
		return msgchannel
	except IndexError:
		return "nullchan"


def getMsgType(line):
	try:
		separate = line.split(" ")
		msgtype = separate[1]
		return msgtype
	except IndexError:
		return "nulltype"


#------------------------------- Api Requests --------------------------------------