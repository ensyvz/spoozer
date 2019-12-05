import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
import time
import dbOperation as db
import threading
import datetime

token = "" 

def msToMinute(ms): # Changes milliseconds to minutes
    second = ms/1000
    minute = second // 60
    second = second%60/100
    time=minute+second
    return time

def auth(): # Spotify token expires after 1 hour so this subprocess will refresh token every 1hour5seconds
    global token
    while True:
        cid = '1613417d61fe44e2a072fbd78f0c684d'
        csec = 'bdef638e4f564c7e9eee361a4440ccb0'
        redir='http://localhost/'

        username = "x5ewxw339c9q44th6z4cpopeu"
        scope= "user-read-currently-playing user-read-playback-state"

        token = util.prompt_for_user_token(username, scope,cid,csec,redir)
        print(token+" | "+datetime.datetime.now().strftime("%H:%M:%S"))
        time.sleep(3605)

def main():
    global token
    cid = '1613417d61fe44e2a072fbd78f0c684d'
    csec = 'bdef638e4f564c7e9eee361a4440ccb0'
    redir='http://localhost/'

    username = "x5ewxw339c9q44th6z4cpopeu"
    scope= "user-read-currently-playing user-read-playback-state"

    token = util.prompt_for_user_token(username, scope,cid,csec,redir)

    sp = spotipy.Spotify(auth=token)
    nowSongName = ""
    nowArtistName=""
    prog = 0
    count = 0
    authOp = threading.Thread(target=auth) # Thread for every hour authentication
    authOp.start()
    while True:
        prevList = nowSongName
        prevProg = prog

        try: # When token expires there will be an error about it 
            result = sp.current_user_playing_track()
            resultPb = sp.current_playback()
        except: # Catching that error and trying to get a new object with new token (if token is not new then there will be an another exception)
            try:
                sp = spotipy.Spotify(auth=token)
            except:
                continue
        if result and resultPb:
            prog = msToMinute(int(result['progress_ms']))

            nowSongName = resultPb['item']['name']
            nowArtistName = resultPb['item']['artists'][0]['name']

            if nowSongName == prevList and prog != prevProg:
                count += 1
            elif prog != prevProg:
                count = 1

            if count == 120:
                db.incCounter(nowSongName,nowArtistName)
            
            time.sleep(0.3)
        else:
            continue
