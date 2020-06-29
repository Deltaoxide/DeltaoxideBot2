import time
from Socket import sendMessage, initChannels
from Settings import *
import requests
import json

if LANGUAGE == "en":
    from Textsen import MSG_FIRST
else:
    from Textstr import MSG_FIRST

commandcoold = {}
spoRefreshTime = 0


f = json.load(open('Spo.json'))

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
    # for chan in initChannels:
        # sendMessage(sock, chan, MSG_FIRST)


def messageCooldown(command, duration):
    if command not in commandcoold or time.time() - commandcoold[command] > duration:
        commandcoold[command] = time.time()
        return True
    else:
        return False


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


def getToken():
    global f
    r = requests.post('https://accounts.spotify.com/api/token', headers={'Authorization': f'Basic {SpoAppToken}'}, data={'grant_type': 'refresh_token', 'refresh_token': f['refresh_token']})
    SpoJson = r.json()
    f['refresh_token'] = SpoJson.get('refresh_token',f['refresh_token'])
    f['access_token'] = SpoJson['access_token']
    f['expires_in'] = SpoJson['expires_in']
    j = json.dumps(f)
    with open('Spo.json', 'w') as file:
        file.write(j)
        file.close()
    return r.ok


def getSong():
    global spoRefreshTime
    global f
    if (time.time() - f['expires_in']) > spoRefreshTime:
        if getToken():
            spoRefreshTime = time.time()
            print('token complete')
        print('new token generated')
    r = requests.get('https://api.spotify.com/v1/me/player/currently-playing',headers={'Authorization': 'Bearer '+f['access_token']})
    print(r.status_code)
    print(r.text)
    if r.ok and not r.status_code == 204 and r.json()['is_playing'] == True :
        SongData = r.json()['item']
        Artists = []
        for i in SongData['artists']:
            Artists.append(i['name'])
        Artists = (',').join(Artists)
        Name = SongData['name']
        Songname = f'{Artists} - {Name}'
    else:
        Songname = '-'
    return Songname


def loadingComplete(line):
    if "End of /NAMES list" in line:
        return False
    else:
        return True
