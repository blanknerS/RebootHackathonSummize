from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import shutil
# from googleapiclient.http import MediaFileUpload


from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from Google import Create_Service

def toDrive():

	gauth = GoogleAuth()

	# Creates local webserver and auto
	# handles authentication.
	gauth.LocalWebserverAuth()
	drive = GoogleDrive(gauth)

	filePath = os.path.expanduser("~/Desktop/subClips")


	for x in os.listdir(filePath):
		if x == "videos.zip":
		    f = drive.CreateFile({'title': x})
		    f.SetContentFile(os.path.join(filePath, x))
		    f.Upload()

	shutil.rmtree(filePath)


# toDrive()


# CLIENT_SECRET_FILE = "client_secrets.json"
# API_NAME = "drive"
# API_VERSION = "v3"
# SCOPES = ["https://www.googleapis.com/auth/drive"]
#
# service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
#
# file_names = ["videos.zip"]
# mime_types = ["application/vnd.google-apps.file"]
#
# for file_name, mime_type in zip(file_names, mime_types):
# 	file_metadata = {
# 	"name": file_name,
# 	}
# 	media = MediaFileUpload(f'{filePath}/videos.zip'.format(file_name), mimetype=mime_type)
#
# 	service.files().create(
# 	body=file_metadata,
# 	media_body=media,
# 	fields="id"
# 	).execute()
























# gauth = GoogleAuth()
# drive = GoogleDrive(gauth)
#
# filepath = os.path.expanduser("~/Desktop/bosie.jpg")
#
# for upload_file in upload_file_list:
# 	gfile = drive.CreateFile({'parents': [{'id': '1S-aDYGzZ7ru5DXMqfg58LURoZwf7MY5x'}]})
# 	# Read file and set it as the content of this instance.
# 	gfile.SetContentFile(upload_file)
# 	gfile.Upload() # Upload the file.
#
#
#
# # from pydrive.auth import GoogleAuth
# # from pydrive.drive import GoogleDrive
# # import json
# # import requests
# #
# # gauth = GoogleAuth()
# # gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
# # drive = GoogleDrive(gauth)
# #
# # # View all folders and file in your Google Drive
# # fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
# # for file in fileList:
# #   print('Title: %s, ID: %s' % (file['title'], file['id']))
# #   # Get the folder ID that you want
# #   if(file['title'] == "images"):
# #       fileID = file['id']
# #
# # file1 = drive.CreateFile({"mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": fileID}]})
# # file1.SetContentFile("2021~03~27@01-05")
# # file1.Upload() # Upload the file.
# # print('Created file %s with mimeType %s' % (file1['title'], file1['mimeType']))
#
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
#
# def toDrive(fp):
#     pass
#     #Login to Google Drive and create drive object
#     g_login = GoogleAuth()
#     g_login.LocalWebserverAuth()
#     drive = GoogleDrive(g_login)
#     # Importing os and glob to find all PDFs inside subfolder
#
#     with open(fp,"r") as f:
#          fn = os.path.basename(f.name)
#          file_drive = drive.CreateFile({'title': fn })
#          file_drive.SetContentString(f.read())
#          file_drive.Upload()
#
#     print ("All files have been uploaded")
#
# toDrive("")
