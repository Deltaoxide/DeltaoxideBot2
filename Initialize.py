import time
# from Socket import sendMessage, initChannels  # Disabled initchannel sendmessage check line 27
from Settings import *
import requests
import json

commandcoold = {}
spoRefreshTime = 0
SpoF = json.load(open('Spo.json'))


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

    sock.send(f"CAP REQ :twitch.tv/commands\r\n".encode('utf-8'))
    # for chan in initChannels:
    #     sendMessage(sock, chan, MSG_FIRST)


def messageCooldown(command, duration):
    if command not in commandcoold or time.time() - commandcoold[command] > duration:
        commandcoold[command] = time.time()
        return True


'''def notifyWeekly(currentdate, weekday, hour, minute):
    if currentdate.isoweekday() == weekday and\
            currentdate.hour == hour and\
            currentdate.minute == minute and currentdate.second == 1:
        return True'''


def stringFormat(string):
    newstring = ''
    charold = ''
    for char in string:
        if charold != char:
            newstring = newstring+char
        charold = char
    return newstring


def convertDay(num,msg_days):
    if num in range(1,8):
        day = msg_days[num]
        return day
    return ''


def getID(login):
    r = requests.get('https://api.twitch.tv/helix/users?login=' + login, headers=AppHeaders)
    return r.json()['data'][0]['id']


def followChan(chan):
    data = {'to_id': getID(chan), 'from_id': BotID}
    headers = {'Client-ID': ClientID, 'Authorization': 'Bearer ' + BotAuth}
    r = requests.post(BaseURL + 'users/follows', headers=headers, data=data)
    return r.ok


def unfChan(chan):
    data = {'to_id': getID(chan), 'from_id': BotID}
    headers = {'Client-ID': ClientID, 'Authorization': 'Bearer ' + BotAuth}
    r = requests.delete(BaseURL + 'users/follows', headers=headers, data=data)
    return r.ok


def isOnline(chan):  # not completed
    data = {}


def getToken():
    global SpoF
    r = requests.post('https://accounts.spotify.com/api/token', headers={'Authorization': f'Basic {SpoAppToken}'}, data={'grant_type': 'refresh_token', 'refresh_token': SpoF['refresh_token']})
    spojson = r.json()
    SpoF['refresh_token'] = spojson.get('refresh_token', SpoF['refresh_token'])
    SpoF['access_token'] = spojson['access_token']
    SpoF['expires_in'] = spojson['expires_in']
    j = json.dumps(SpoF)
    with open('Spo.json', 'w') as file:
        file.write(j)
        file.close()
    return r.ok


def getSong():
    global spoRefreshTime
    global SpoF
    if (time.time() - SpoF['expires_in']) > spoRefreshTime:

        if getToken():
            spoRefreshTime = time.time()

    r = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers={'Authorization': 'Bearer ' + SpoF['access_token']})

    if r.ok and not r.status_code == 204 and r.json()['is_playing'] == True :
        songdata = r.json()['item']
        artists = []
        for i in songdata['artists']:
            artists.append(i['name'])
        artists = (',').join(artists)
        name = songdata['name']
        songname = f'{artists} - {name}'
    else:
        songname = '-'
    return songname


def loadingComplete(line):
    if "End of /NAMES list" in line:
        return False
    else:
        return True
