import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyDictionary import PyDictionary
import toAudio
import toText
import getVideoClips
import summary
import basicEmail
import toGoogleDrive

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        windowWidth = 350
        windowHeight = 200
        self.setGeometry(500, 150, windowWidth, windowHeight)
        self.setFixedSize(windowWidth, windowHeight)
        self.setStyleSheet("color: white; background:rgb(86, 133, 148)")
        self.setWindowTitle("Welcome")

        self.intro_label = QLabel(self)
        self.intro_label.setText("""Hello and welcome all, this is a more in depth look at Summize, our Project Reboot creation. On a basic level Summize helps teachers summarize and define zoom lessons for students who may have missed a lecture or are in another time zone. We sought to solve the disconnect between students who miss zoom class and the class as a whole. \n\nPress Continue to begin!""") # <-- text for intro
        self.intro_label.setFont(QFont('Arial', 15))
        self.intro_label.setWordWrap(True)
        self.intro_label.setGeometry(5, 5, 335, 195)
        self.intro_label.setAlignment(QtCore.Qt.AlignLeft)

        linkTemplate = '<a href={0}>{1}</a>'
        summize_link = 'https://docs.google.com/document/d/1WA9YZJMsV6hrvMnzTu4zoOrtj2GFY8p8rK7h78Ul-Vg/edit?usp=sharing'

        self.label1 = HyperlinkLabel(self)
        self.label1.setText(linkTemplate.format(summize_link, '(Here for more)'))
        self.label1.setFont(QFont('Arial', 11))
        self.label1.setStyleSheet("color: rgb(156, 156, 156)")
        self.label1.setGeometry(55, 135, 100, 10)

        self.leave_intro_button = QPushButton("Continue", self)
        self.leave_intro_button.setStyleSheet("background:rgb(133, 133, 133)")
        self.leave_intro_button.setGeometry(265, 155, 65, 30)
        self.leave_intro_button.clicked.connect(self.filePathAndWords)

    def filePathAndWords(self):
        self.w = firstScreen()
        self.w.show()
        self.hide()

class firstScreen(QMainWindow):

    def __init__(self):
        super().__init__()

        windowWidth = 350
        windowHeight = 200
        self.setGeometry(500, 150, windowWidth, windowHeight)
        self.setFixedSize(windowWidth, windowHeight)
        self.setStyleSheet("color: white; background:rgb(86, 133, 148)")

        self.setWindowTitle("Word Finder")
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.path_label = QLabel(self)
        self.path_label.setText("Full path to video:")
        self.path_label.setGeometry(15, 20, 150, 15)

        self.path_text = QLineEdit(self)
        self.path_text.setGeometry(15, 40, 300, 15)

        self.words_to_find_label = QLabel(self)
        self.words_to_find_label.setText("Words to find:")
        self.words_to_find_label.setGeometry(15, 75, 100, 15)

        self.words_to_find_text = QLineEdit(self)
        self.words_to_find_text.setGeometry(15, 95, 300, 15)

        self.words_hint_label = QLabel(self)
        self.words_hint_label.setText("(Seperate words via: , ) ie: this, that, those")
        self.words_hint_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.words_hint_label.setGeometry(15, 115, 350, 15)

        self.go_button = QPushButton("Go", self)
        self.go_button.setStyleSheet("background:rgb(133, 133, 133)")
        self.go_button.setGeometry(265, 155, 50, 30)
        self.go_button.clicked.connect(self.on_click)

    def on_click(self):
        filePath = self.path_text.text()
        keyWords = self.words_to_find_text.text()
        self.progressScreenShow(filePath, keyWords)
        return keyWords, filePath

    def progressScreenShow(self, filePath, keyWords):
        self.w = progressScreen(filePath, keyWords)
        self.w.show()
        self.hide()

class progressScreen(QMainWindow):
    def __init__(self, filePath, keyWords):
        super().__init__()

        windowWidth = 350
        windowHeight = 130
        self.setGeometry(500, 150, windowWidth, windowHeight)
        self.setFixedSize(windowWidth, windowHeight)
        self.setStyleSheet("color: white; background:rgb(86, 133, 148)")

        self.setWindowTitle("Processing")
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.progress_label = QLabel(self)
        self.progress_label.setText("Status: ")
        self.progress_label.setFont(QtGui.QFont("Arial", 17,weight=QtGui.QFont.Bold))
        self.progress_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.progress_label.setGeometry(15, 10, 100, 15)

        self.summary_label = QLabel(self)
        self.summary_label.setText("Sumary  -----")
        self.summary_label.setFont(QFont('Arial', 15))
        self.summary_label.setStyleSheet("color: black")
        self.summary_label.setGeometry(30, 40, 100, 15)

        self.snippets_and_timestamps_label = QLabel(self)
        # I called this snts for short
        self.snippets_and_timestamps_label.setText("Snippets and Timestamps-----")
        self.snippets_and_timestamps_label.setFont(QFont('Arial', 15))
        self.snippets_and_timestamps_label.setStyleSheet("color: black")
        self.snippets_and_timestamps_label.setGeometry(30, 70, 200, 15)

        desktopPath = os.path.expanduser("~/Desktop")

        self.loading_label = QLabel(self)
        self.loading_label.setText("Error")
        self.loading_label.setStyleSheet("color: rgb(173, 33, 33)")
        self.loading_label.setGeometry(130, 40, 30, 15)

        self.snts_label = QLabel(self)
        self.snts_label.setText("Error")
        self.snts_label.setStyleSheet("color: rgb(173, 33, 33)")
        self.snts_label.setGeometry(240, 70, 200, 15)

        self.continue_label = QLabel(self)
        self.continue_label.setText("")
        self.continue_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.continue_label.setGeometry(80, 95, 155, 30)

        try:
            toAudio.make_audio(filePath)
            audioPath = os.path.expanduser("~/Desktop/myAudio.flac")
            toText.upload_to_bucket("myAudio", audioPath, "sttproject")

            transcriptText = toText.get_transcript("gs://sttproject/myAudio")
            print(transcriptText)
            summarizedClass = summary.summarize(transcriptText)

            self.loading_label.setStyleSheet("color: rgb(9, 176, 0)")
            self.loading_label.setText("✅")

            print("keyWords: ",keyWords)

            names_and_ts = getVideoClips.get_clips(filePath, keyWords)

            self.snts_label.setStyleSheet("color: rgb(9, 176, 0)")
            self.snts_label.setText("✅")

            self.continue_label.setText("Press continue -->")

            print("done")

        except:
            print("error")

            self.back_button = QPushButton("Restart", self)
            self.back_button.setStyleSheet("background:rgb(133, 133, 133)")
            self.back_button.setGeometry(15, 95, 100, 30)
            self.back_button.clicked.connect(self.toHomeAagin)

        self.continue_to_email_button = QPushButton("Continue", self)
        self.continue_to_email_button.setStyleSheet("background:rgb(133, 133, 133)")
        self.continue_to_email_button.setGeometry(240, 95, 100, 30)
        self.continue_to_email_button.clicked.connect(partial(self.emailDrafting, summarizedClass, names_and_ts))

    def toHomeAagin(self):
        self.w = StartWindow()
        self.w.show()
        self.hide()
        # print(summarizedClass)

        # self.draftEmaillScreen(summarizedClass)

    def emailDrafting(self, summary, names_and_ts):
        self.w = draftEmaillScreen(summary, names_and_ts)
        self.w.show()
        self.hide()

class draftEmaillScreen(QMainWindow):

    def __init__(self, summary, names_and_ts): #summary here ie (self, summary)
        super().__init__()

        windowWidth = 550
        windowHeight = 240
        self.setGeometry(500, 150, windowWidth, windowHeight)
        self.setFixedSize(windowWidth, windowHeight)
        self.setStyleSheet("color: white; background:rgb(86, 133, 148)")

        self.summaryToPass = summary
        self.names_and_timestamps = names_and_ts

        self.setWindowTitle("Email Info")
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.own_email_label = QLabel(self)
        self.own_email_label.setText("Own email:")
        self.own_email_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.own_email_label.setGeometry(15, 15, 325, 15)

        self.own_email_text = QLineEdit(self)
        self.own_email_text.setGeometry(15, 35, 320, 15)

        self.factor_key_label = QLabel(self)
        self.factor_key_label.setText("Key:")
        self.factor_key_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.factor_key_label.setGeometry(350, 15, 235, 15)

        self.factor_key_text = QLineEdit(self)
        self.factor_key_text.setGeometry(350, 35, 180, 15)
        self.factor_key_text.setEchoMode(QLineEdit.Password)

        self.group_name_label = QLabel(self)
        self.group_name_label.setText("Group Name:")
        self.group_name_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.group_name_label.setGeometry(15, 60, 350, 15)

        self.group_name_text = QLineEdit(self)
        self.group_name_text.setGeometry(15, 80, 250, 15)

        self.teacher_name_label = QLabel(self)
        self.teacher_name_label.setText("Teacher Name:")
        self.teacher_name_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.teacher_name_label.setGeometry(285, 60, 235, 15)

        self.teacher_name_text = QLineEdit(self)
        self.teacher_name_text.setGeometry(280, 80, 250, 15)

        self.zoom_link_label = QLabel(self)
        self.zoom_link_label.setText("Zoom Link:")
        self.zoom_link_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.zoom_link_label.setGeometry(15, 105, 350, 15)

        self.zoom_link_text = QLineEdit(self)
        self.zoom_link_text.setGeometry(15, 125, 355, 15)

        self.zoom_password_label = QLabel(self)
        self.zoom_password_label.setText("Zoom Password:")
        self.zoom_password_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.zoom_password_label.setGeometry(385, 105, 150, 15)

        self.zoom_password_text = QLineEdit(self)
        self.zoom_password_text.setGeometry(385, 125, 145, 15)

        self.recipients_label = QLabel(self)
        self.recipients_label.setText("Recipients Email(s):")
        self.recipients_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.recipients_label.setGeometry(15, 150, 150, 15)

        self.recipients_text = QLineEdit(self)
        self.recipients_text.setGeometry(15, 170, 360, 45)

        self.recipients_hint = QLabel(self)
        self.recipients_hint.setText("(Seperate emails with a comma) ie. example@gmail.com, example2@gmail.com")
        self.recipients_hint.setStyleSheet("color: rgb(217, 217, 217)")
        self.recipients_hint.setFont(QFont('Arial', 11))
        self.recipients_hint.setGeometry(15, 220, 370, 15)

        self.create_button = QPushButton("Create", self)
        self.create_button.setStyleSheet("background:rgb(133, 133, 133)")
        self.create_button.setGeometry(410, 170, 100, 45)
        self.create_button.clicked.connect(self.on_click)

    def on_click(self):
        summary = self.summaryToPass
        names_and_ts = self.names_and_timestamps
        teacher_email = self.own_email_text.text()
        teacher_key = self.factor_key_text.text()
        group_name = self.group_name_text.text()
        teacher_name = self.teacher_name_text.text()
        zoom_link = self.zoom_link_text.text()
        zoom_password = self.zoom_password_text.text()
        recipients = self.recipients_text.text()
        self.toEmailPreview(teacher_email, teacher_key, group_name, teacher_name, zoom_link, zoom_password, recipients, summary, names_and_ts)
        # return teacher_email, teacher_key, group_name, teacher_name, zoom_link, zoom_password,

    def toEmailPreview(self, teacherEmail, teacherKey, groupName, teacherName, zoomLink, zoomPassword, recipients, summary, names_and_ts):
        self.w = emailPreviewWindow(teacherEmail, teacherKey, groupName, teacherName, zoomLink, zoomPassword, recipients, summary, names_and_ts)
        self.w.show()
        self.hide()

class emailPreviewWindow(QMainWindow):
    def __init__(self, teacherEmail, teacherKey, groupName, teacherName, zoomLink, zoomPassword, recipients, summary, names_and_ts): #add later:
        super().__init__()
        windowWidth = 550
        windowHeight = 400
        self.setGeometry(500, 150, windowWidth, windowHeight)
        self.setFixedSize(windowWidth, windowHeight)
        self.setStyleSheet("color: white; background:rgb(86, 133, 148)")

        # summary = """I didn't know you had it all figured out life piece together on mine was piece of part. How can I know you know, I see you out there? Let me stupid my head held high swinging at its all-time low success is in the eye of the beholder and I behold all I'm in control. I need you, please please don't go I need you."""
        # zoomLink = "LWVHO"
        # zoomPassword = "lwkjfhl"

        self.setWindowTitle("Email Draft")
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.summary_intro_label = QLabel(self)
        self.summary_intro_label.setText("Summary:")
        self.summary_intro_label.setFont(QtGui.QFont("Arial",weight=QtGui.QFont.Bold))
        self.summary_intro_label.setWordWrap(True)
        self.summary_intro_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.summary_intro_label.setGeometry(15, 15, 100, 15)

        self.summary_label = QLabel(self)
        self.summary_label.setText(f"{summary}")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("color: rgb(209, 209, 209)")
        self.summary_label.setGeometry(30, 35, 500, 80)

        self.words_found_intro_label = QLabel(self)
        self.words_found_intro_label.setText("Words + Timestamps:")
        self.words_found_intro_label.setFont(QtGui.QFont("Arial",weight=QtGui.QFont.Bold))
        self.words_found_intro_label.setWordWrap(True)
        self.words_found_intro_label.setStyleSheet("color: rgb(217, 217, 217)")
        self.words_found_intro_label.setGeometry(15, 125, 200, 15)

        dictionary=PyDictionary()

        # names_and_ts = ['blood', '0-00-01', 'blood', '0-00-22', 'blood', '0-01-08', 'mirrors', '0-01-26', 'blood', '0-00-22', 'blood', '0-00-22', 'blood', '0-00-22', 'blood', '0-00-22',]
        times_and_words = names_and_ts
        timestamps = times_and_words[1::2]
        convertedTimeStamps = []
        for i in timestamps:
            convertedTimeStamps.append(i.replace("-", ":"))
        words = times_and_words[0::2]

        keyTermsIntro = ""
        for time, name in zip(convertedTimeStamps, words):
            keyTermsIntro += f"\n{name} --------- Found @{time}"
            # keyTermsIntro += '\n' + name + ' '  +POS+ f'\n       Found @ {time}' # <-- TIMESTAMP

        self.words_found_label = QLabel(self)
        self.words_found_label.setText(f"{keyTermsIntro}")
        self.words_found_label.setAlignment(QtCore.Qt.AlignLeft)
        self.words_found_label.setWordWrap(True)
        self.words_found_label.setFont(QFont('Arial', 11))
        self.words_found_label.setStyleSheet("color: rgb(209, 209, 209)")
        self.words_found_label.setGeometry(30, 150, 500, 90)

        self.whole_video_intro = QLabel(self)
        self.whole_video_intro.setText("Full Video:")
        self.whole_video_intro.setFont(QtGui.QFont("Arial",weight=QtGui.QFont.Bold))
        self.whole_video_intro.setWordWrap(True)
        self.whole_video_intro.setStyleSheet("color: rgb(217, 217, 217)")
        self.whole_video_intro.setGeometry(15, 260, 200, 15)

        linkTemplate = '<a href={0}>{1}</a>'

        self.label1 = HyperlinkLabel(self)
        self.label1.setText(linkTemplate.format(zoomLink, 'Zoom link'))
        self.label1.setGeometry(30, 285, 500, 20)

        self.whole_video_password_label = QLabel(self)
        self.whole_video_password_label.setText(f" Video password: {zoomPassword}")
        self.whole_video_password_label.setAlignment(QtCore.Qt.AlignLeft)
        self.whole_video_password_label.setWordWrap(True)
        self.whole_video_password_label.setStyleSheet("color: rgb(209, 209, 209)")
        self.whole_video_password_label.setGeometry(30, 310, 500, 20)

        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet("background:rgb(133, 133, 133)")
        self.send_button.setGeometry(410, 345, 100, 45)
        self.send_button.clicked.connect(self.on_click)

        self.back_button = QPushButton("Restart", self)
        self.back_button.setStyleSheet("background:rgb(133, 133, 133)")
        self.back_button.setGeometry(15, 345, 100, 45)
        self.back_button.clicked.connect(self.toHomeAagin)

        self.teacherEmail = teacherEmail
        self.teacherKey = teacherKey
        self.groupName = groupName
        self.teacherName = teacherName
        self.zoomLink = zoomLink
        self.zoomPassword = zoomPassword
        self.recipients = recipients
        self.summary = summary
        self.names_and_ts = names_and_ts

    def toHomeAagin(self):
        self.w = StartWindow()
        self.w.show()
        self.hide()

    def on_click(self):
        toGoogleDrive.toDrive()
        basicEmail.send_email(self.teacherEmail, self.teacherKey, self.groupName, self.teacherName, self.zoomLink, self.zoomPassword, self.recipients, self.summary, self.names_and_ts)

class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        # self.setStyleSheet('font-size: 35px')
        self.setOpenExternalLinks(True)
        self.setParent(parent)




stylesheet = """
    MainWindow {
        background-repeat: no-repeat;
        background-position: center;
    }
"""

def main():

    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
