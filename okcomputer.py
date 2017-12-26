#Used Libraries
from userclass import User
from computerclass import Computer
from functionclass import clearScreen, speak
import os

#Declared Variables
username = User('')
computer = Computer('')
tempanswer = ''

#Window Size
os.system('mode con: cols=35 lines=15')

def userInput():
	#answer = "roll two dice"
	answer = computer.getInput()
	print answer

	tempanswer = answer

	if answer == 0:
		return 0

	if answer.find('weather') > -1 :
		computer.tellWeather()
		return 0
	if answer.find('time') > -1 :
		computer.tellTime()
		return 0
	if answer.find('remember') > -1 :
		username.saveReminder(answer)
		return 0
	if answer.find("what_s new") > -1 or answer.find("in the news") > -1 or answer.find("read the news") > -1 or answer.find("headlines") > -1 or answer.find("what_s the news") > -1 or answer.find("what_s the new") > -1 or answer.find("news") > -1:
		computer.news()
		return 0
	if answer.find("have to do") > -1 or answer.find("on the schedule") > -1 or answer.find("on my schedule") > -1 or answer.find("do today") > -1 or answer.find("something to do") > -1 or answer.find("be doing") > -1 or answer.find("needed to be") > -1 or answer.find("to do") > -1 or answer.find("going on today") > -1 or answer.find("reminders") > -1:
		username.sayReminder()
		return 0
	if answer.find("my name is") > -1 or answer.find("can call me") > -1 or answer.find("the name is ") > -1 or answer.find("call me") > -1:
		username.nameUser(answer)
		return 0
	if answer.find("my name") > -1:
		username.sayUserName()
		return 0
	if answer.find("your name is") > -1 or answer.find("name will be") > -1 or answer.find("can I call you") > -1:
		computer.nameComputer(answer)
		return 0
	if answer.find("your name") > -1 or answer.find("call you") > -1 :
		computer.sayComputerName()
		return 0
	if answer.find("good morning") > -1 or answer.find("morning") > -1:
		speak("Good Morning") 
		username.sayUserName()
		computer.goodMorning()
		return 0
	if answer.find("roll dice") > -1 or answer.find("dice") > -1 :
		computer.rollDice(answer)
		return 0
	if answer.find("flip a coin") > -1 or answer.find("coin") > -1 :
		computer.flipCoin()
		return 0
	if answer.find("tell me a joke") > -1 or answer.find("joke") > -1 :
		computer.momJoke()
		return 0
	if answer.find(' ') == -1 :
		answer = computer.singleListCheck(answer)
		if answer == None:
			computer.addUnknownResponse(tempanswer)
		return 0
	if answer.find(' ') > -1 :
		answer = computer.multipleListCheck(answer)
		if answer == None:
			computer.addUnknownResponse(tempanswer)
		return 0
		
	return 0

def aiEngine():
	#clearScreen()
	userInput()
	#userrequest = raw_input('Press Enter to talk.\n:> ')
	#while userrequest != 'exit':		
	#	userInput()
	#	aiEngine()
	#else:
	#	clearScreen()
	#	print 'Good Day!'
	#	sys.exit()

#if __name__ == '__main__':
#    aiEngine()



# CREATE DATABASE AND TABLES
#====================================================================================================================================================================================================		

#Create Database - errors but creates db
#cursor.execute('CREATE DATABASE "okcomputer.db"')	

# Drop table
#cursor.execute('drop table userinput')		

# Create userinput table
#cursor.execute('''CREATE TABLE `userinput` (`UserInputNum` INTEGER PRIMARY KEY AUTOINCREMENT,`UserInputText` VARCHAR(500) NOT NULL)''')

# Create answer table
# cursor.execute('''CREATE TABLE `learnedresponse` (`LearnedResponseNum` INTEGER PRIMARY KEY AUTOINCREMENT,`LearnedResponseText` VARCHAR(500) NOT NULL,`UserInputNum` INTEGER NOT NULL)''')

# Create knownresponse table
#cursor.execute('''CREATE TABLE `knownresponse` (`KnownResponseNum` INTEGER PRIMARY KEY AUTOINCREMENT,`KnownResponseText` VARCHAR(500) NOT NULL,`KnownResponseAnswer` VARCHAR(500) NOT NULL)''')

# Create userpreference table
#cursor.execute('''CREATE TABLE `userpreference` (`UserPreferenceNum` INTEGER PRIMARY KEY AUTOINCREMENT,`UserPreferenceName` VARCHAR(500) NOT NULL,`UserPreferenceValue` VARCHAR(500) NOT NULL)''')

# Create reminder table
# cursor.execute('''CREATE TABLE `reminder` (`ReminderNum` INTEGER PRIMARY KEY AUTOINCREMENT,`ReminderText` VARCHAR(500) NOT NULL,`ReminderDateTime` datetime NOT NULL,'IsFinished' INTEGER)''')
# cnx.commit()

# Syntax to insert rows
# select ui.UserInputText, lr.LearnedResponseText from userinput ui INNER JOIN learnedresponse lr ON ui.UserInputnum = lr.UserInputnum 	AND lr.LearnedResponseText LIKE '%say%' 
# INSERT INTO knownresponse VALUES (NULL,'what_s up girl','whats up')
# UPDATE knownresponse SET KnownResponseAnswer = 'Nothing. Whats up?' WHERE KnownResponseNum = 10
#====================================================================================================================================================================================================
					 