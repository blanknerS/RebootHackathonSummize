#Blake Ankner
import toText
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from datetime import datetime as dt
import datetime
import os
import zipfiles

def get_clips(path, words):
    date = dt.now().strftime("%Y~%m~%d@%H-%M")
    videoFile = mp.VideoFileClip(path)
    desktopPath = os.path.expanduser("~/Desktop")
    audioPath = os.path.expanduser("~/Desktop/myAudio.flac")
    toText.upload_to_bucket("myAudio", audioPath, "sttproject")
    times_and_words = toText.transcribe_gcs_with_word_time_offsets("gs://sttproject/myAudio", words)

    os.remove(f"{desktopPath}/myAudio.flac")
    timestamps = times_and_words[1::2]
    words = times_and_words[0::2]
    convertedTimeStamps = []
    clip = 0
    for time, name in zip(timestamps, words):
        if time - 10.0 < 0:
            start = 0
        else:
            start = time - 10

        if time + 10 > videoFile.duration:
            end = videoFile.duration
        else:
            end = time + 10
        if not os.path.exists(f"{desktopPath}/subClips"):
            os.makedirs(f"{desktopPath}/subClips")
        if not os.path.exists(f"{desktopPath}/subClips/{date}"):
            os.makedirs(f"{desktopPath}/subClips/{date}")

        convertedTimeStamp = str(datetime.timedelta(seconds=time))[:7]
        convertedTimeStamp = convertedTimeStamp.replace(":", "-")
        convertedTimeStamps.append(name)
        convertedTimeStamps.append(convertedTimeStamp)

        smallClip = ffmpeg_extract_subclip(path, start, end, targetname=f"{desktopPath}/subClips/{date}/{name}@{convertedTimeStamp}.mp4")
        clip = clip + 1
    zipfiles.zippIt()
    return convertedTimeStamps

# print(convertedTimeStamps)
#
# get_clips("/Users/blakeankner/Desktop/CLIP1.mp4", "apple, banana, peach")
