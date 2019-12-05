import sqlite3

from deezloader import Login

import dbOperation as db
import time

def download(outputFolder):
    token = "884d9cf88f80e652ea8d78b64ed7cd1a60e7c7ecf2ee2c74811837ece0291b477e9c29e8e638b6a5c5b37cab0bf13b726cfb27fc09e55ecb74f5785dccee18c96a84220527d166b527f830c857a7b5128f4e3d194b78d8cb63bd6467c7d8c4e4"
    downloa = Login(token)
    
    quality = "FLAC"
    output = outputFolder
    recursive_quality = False
    recursive_download = False
    not_gui=False
    song = ""
    artist = ""

    downQueue = db.getDownloadQueue()

    for songs in downQueue:
        song = songs[0]
        artist = songs[1]

        downloa.download_name(
        artist,song,output,
        quality,recursive_quality,
        recursive_download,not_gui
        )
        db.downloaded(song,artist)

def main(outputFolder): 
    while True:
        download(outputFolder)
        time.sleep(3600)