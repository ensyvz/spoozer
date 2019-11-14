import sqlite3
import os 

path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'spoozer.db')

def getCounter(songName,artistName):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("SELECT counter FROM songs WHERE songName=?",(songName,))
    counter = cur.fetchone()
    if counter is None:
        addSong(songName,artistName)
        con.close()
        return 0
    else:
        con.close()
        return counter[0]

def addSong(songName,artistName):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("INSERT INTO songs (songName,artistName,counter,isDownloaded) VALUES (?,?,1,0)",(songName,artistName,))
    con.commit()
    con.close()

def incCounter(songName,artistName):
    con = sqlite3.connect(db)
    cur = con.cursor()
    counter = getCounter(songName,artistName)+1
    cur.execute("UPDATE songs SET counter=? WHERE songName=?",(counter,songName,))
    con.commit()
    con.close()

def getDownloadQueue():
    con = sqlite3.connect(db)
    cur = con.cursor()
    rows = cur.execute("SELECT songName,artistName FROM songs WHERE isDownloaded=0 and counter>5")
    queue = []
    for row in rows:
        queue += [[row[0],row[1]]]
    con.close()
    return queue

def downloaded(songName,artistName):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("UPDATE songs SET isDownloaded=1 WHERE songName=? and artistName=?",(songName,artistName,))
    con.commit()
    con.close()