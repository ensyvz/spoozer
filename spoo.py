import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
import time
import dbOperation as db

def msToMinute(ms):
    second = ms/1000
    minute = second // 60
    second = second%60/100
    time=minute+second
    return time

def auth():
    while True:
        cid = '1613417d61fe44e2a072fbd78f0c684d'
        csec = 'bdef638e4f564c7e9eee361a4440ccb0'
        redir='http://localhost'

        username = "x5ewxw339c9q44th6z4cpopeu"
        scope= "user-read-currently-playing user-read-playback-state"

        token = util.prompt_for_user_token(username, scope,cid,csec,redir)
        time.sleep(3500)

def main():
    cid = '1613417d61fe44e2a072fbd78f0c684d'
    csec = 'bdef638e4f564c7e9eee361a4440ccb0'
    redir='http://localhost'

    username = "x5ewxw339c9q44th6z4cpopeu"
    scope= "user-read-currently-playing user-read-playback-state"

    token = util.prompt_for_user_token(username, scope,cid,csec,redir)

    sp = spotipy.Spotify(auth=token)
    nowSongName = ""
    nowArtistName=""
    prog = 0
    count = 0
    authOp = threading.Thread(target=auth) 
    authOp.start()
    while True:
        prevList = nowSongName
        prevProg = prog

        result = sp.current_user_playing_track()

        if result:
            prog = msToMinute(int(result['progress_ms']))

            resultPb = sp.current_playback()

            nowSongName = resultPb['item']['name']
            nowArtistName = resultPb['item']['artists'][0]['name']

            if nowSongName == prevList and prog != prevProg:
                count += 1
            elif prog != prevProg:
                count = 1

            print(count)

            if count == 150:
                db.incCounter(nowSongName,nowArtistName)
            time.sleep(0.5)
        else:
            continue
