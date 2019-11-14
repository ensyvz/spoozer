import threading
import time
import spoo
import zer

outputFolder = input("Download Folder Path : ")

deezer = threading.Thread(target=zer.main,args=(outputFolder,))
deezer.start()
spoo.main()


