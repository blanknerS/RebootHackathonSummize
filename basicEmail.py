#ANDREW RODRIGUEZ

#imports
import smtplib
from email.message import EmailMessage
from PyDictionary import PyDictionary
from datetime import datetime
import os

#NEEDED INPUT FOR THIS PROGRAM, Teacher name, recipitants emails, key terms, key terms folder link, zoom link, zoom password

def send_email(teacherEmail, teacherKey, groupName, teacherName, zoomLink, zoomPassword, recipients, summary, names_and_ts):

	#Dictonary for words
	dictionary=PyDictionary()

	#Email to send from
	EMAIL_ADDRESS = teacherEmail
	EMAIL_PASSWORD = teacherKey

	#For people receiving the email
	recipients = [recipients]


	#Text feild for Name of class and date
	today = datetime.today().strftime("%m-%d-%Y")
	date = today
	section = groupName
	times_and_words = names_and_ts
	timestamps = times_and_words[1::2]
	convertedTimeStamps = []
	for i in timestamps:
		convertedTimeStamps.append(i.replace("-", ":"))

	words = times_and_words[0::2]
	# print(words)

	#Combine the two
	classHeader = section + ', ' + date

	#Name of whoever is receiving, IE Class, Freinds, Internation Students
	grp = groupName

	#Create full greeting,
	greeting = "Hello " + grp + ",\n\nHere is the class summary for today: \n \n"

	#A basic sumamry # <-- SUMARY
	classSum = summary

	# print(convertedTimeStamps)
	# print(words)

	#For list of key words
	keyTermsIntro = '\n\nHere are some key terms from throughout the class, you will find they also have time stamps and part of speech'
	for time, name in zip(convertedTimeStamps, words):
		# print(dictionary.meaning(name), type(dictionary.meaning(name)))
		# POS = ', '.join(dictionary.meaning(name))
		keyTermsIntro += '\n\n' + name + ' ' + f'\n ---- Found @ {time}' # <-- TIMESTAMP


	keyTermsTotal = keyTermsIntro

	#Link to folder
	# clipsLink = 'The clips ' # <-- LINK TO FOLDER

	#Final Message for Terms
	keyTermsFinal = keyTermsTotal + '\n\nIf you want to check out those clips on their own, they will be in our class folder in Drive!\n              '

	#Zoom link
	zoomLink = zoomLink

	#Zoom Password
	zoomPassword = zoomPassword

	#Zoom Stuff Formated
	zoomFull = '\n\n\nYou can find the whole class recording right here: \n              ' + zoomLink + '\nThe password is: \n              ' + zoomPassword

	#Outro Stuff
	teachersName = teacherName
	fullOutro = '\n\nThat is all for today folks, as always if you have any questions email me, \n         Best, \n              ' + teachersName

	msg = EmailMessage()
	msg['Subject'] = classHeader
	msg['From'] = EMAIL_ADDRESS
	msg['To'] = recipients


	msg.set_content(greeting + classSum + keyTermsFinal + zoomFull + fullOutro)

	# with open("snippetVideos.zip", 'rb') as zip:
	# 	msg.add_attachment(zip.read(), maintype='application', subtype='octet-stream', filename=zip.name)

	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
	    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
	    smtp.send_message(msg)

# send_email("HackathonNotesMadeEasy2021@gmail.com", "tccz rdgh qiag zhge", "eg", "eg", "eg", "eg", "blakeyankner@gmail.com", "SUMMARY", ['how', '0-00-00', 'blood', '0-00-01', 'blood', '0-00-22', 'how', '0-00-49', 'blood', '0-01-08'])
