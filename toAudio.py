#Blake Ankner
import moviepy.editor as mp
import subprocess
import os

def make_audio(videoPath):
    desktopPath = os.path.expanduser("~/Desktop")
    clip = mp.VideoFileClip(videoPath)
    clip.audio.write_audiofile(f"{desktopPath}/myAudio.wav")
    subprocess.call(['avconv', '-i', f'{desktopPath}/myAudio.wav', '-y', '-ar', '48000', '-ac', '1', f'{desktopPath}/myAudio.flac'])
    os.remove(f"{desktopPath}/myAudio.wav")

# make_audio("/Users/blakeankner/Desktop/CLIP1.mp4")
