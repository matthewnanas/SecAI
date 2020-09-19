from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

gauth = GoogleAuth()

gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


def upload_video(title):
    video = VideoFileClip("./output.avi")
    ending_time = video.duration

    ffmpeg_extract_subclip("./output.avi", ending_time - 15, ending_time,
                           targetname="output_trim.avi")

    path = "./output.avi"
    i = 0
    fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    print("\nSelect the number corresponding to the folder!")
    for file in fileList:
        print(f"{i}. {file['title']}")
        i += 1

    iterator = int(input())
    drive_id = fileList[iterator]["id"]

    f = drive.CreateFile({'title': str(title), 'parents': [{'id': str(drive_id)}]})
    f.SetContentFile(os.path.join(path))
    f.Upload()
    f = None
