#Used Libraries
import os, sys, time
import sqlite3
from datetime import datetime
from functionclass import speak

#Declared Variables
cnx = sqlite3.connect('E:\\Python27\\okcomputer.db')
cnx.text_factory = str
cursor = cnx.cursor()

class User(object):
	def __init__(self, username):
		self.username = username

	#Print Player Attributes
	def __str__(self):
		return "Username: %s" %(self.username)

	def sayUserName(self):
		if self.username == "":
			speak("I'm sorry. But you haven't given me your name yet.")
		else:
			speak(self.username)

	def nameUser(self,str):
		int = str.find("is ")
		userName = str[int+3:]
		self.username = userName

		cursor.execute("SELECT UserPreferenceValue FROM userpreference WHERE UserPreferenceName = 'UserName'")
		foundRow = cursor.fetchone()
		foundRow = foundRow[0]
		cursor.execute("UPDATE userpreference SET UserPreferenceValue = '%s' WHERE UserPreferenceName = 'UserName'" % (userName))
		cnx.commit()
		speak("Ok. I will call you " + userName)
		return userName

	def saveReminder(self,str):
	    cursor.execute('''INSERT INTO reminder(ReminderNum,ReminderText,ReminderDateTime,IsFinished) VALUES(?,replace(?,"'","_"),datetime("now","-8 Hour"),?)''', (None,str[9:],0))
	    cnx.commit()
	    speak("Ok. I will remember that")
    
	def sayReminder(self):
		mytime = 0
		for reminder in cursor.execute("SELECT ReminderText,((strftime('%s','now','-8 Hour')-strftime('%s',ReminderDateTime))/60) AS MinutesSince FROM reminder WHERE IsFinished != 1"):
			if reminder[1] > 60:
				mytime = reminder[1] / 60
				print "%d hour's ago you said, '%s'." %(mytime,reminder[0])
				speak("%d hour's ago you said " % mytime + reminder[0])
			else:
				speak(str(reminder[1]) + "minutes ago you said" + reminder[0])