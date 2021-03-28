#Blake Ankner
import os
import zipfile
import requests
from datetime import datetime

def zippIt():

    desktopPath = os.path.expanduser("~/Desktop")
    fantasy_zip = zipfile.ZipFile(f'{desktopPath}/subClips/videos.zip', 'w')
    date = datetime.now().strftime("%Y~%m~%d@%H-%M")

    for folder, subfolders, files in os.walk(f'{desktopPath}/subClips'):
        for file in files:
            if file.endswith('.mp4'):
                fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), f'{desktopPath}/subClips/{date}'), compress_type = zipfile.ZIP_DEFLATED)
    fantasy_zip.close()

# zippIt()
