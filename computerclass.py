#Used Libraries
import urllib2, os, sys, time
import sqlite3
import speech_recognition as sr
from functionclass import clearScreen,speak
from random import randint
from word2number import w2n

#Declared Variables
cnx = sqlite3.connect('E:\\Python27\\okcomputer.db')
cnx.text_factory = str
cursor = cnx.cursor()
r = sr.Recognizer()

class Computer(object):
	def __init__(self, computername):
		self.computername = computername

	#Print Player Attributes
	def __str__(self):
		return "Computer name: %s" %(self.computername)

	def showTableData(self):
		i = 0
		for row in cursor.execute("SELECT ui.UserInputText,lr.LearnedResponseText FROM userinput ui INNER JOIN learnedresponse lr ON ui.UserInputNum = lr.UserInputNum WHERE ui.UserInputText NOT LIKE '%'||(SELECT KnownResponseText FROM knownresponse)||'%'"):
				i = i + 1
				print str(i)+'.',row
		raw_input("\nPress Enter key to continue.")
		clearScreen()
		i = 0
		for row in cursor.execute("SELECT knownresponse.KnownResponseText,knownresponse.KnownResponseAnswer FROM knownresponse "):
				i = i + 1
				print str(i)+'.',row
		raw_input("\nPress Enter key to continue.")

	def sayComputerName(self):
		if self.computername == "":
			speak("I'm sorry. But you haven't given me a name yet.")
		else:
			speak("My name is " + self.computername)

	def nameComputer(self,str):
		int = str.find("is ")
		computerName = str[int+3:]
		self.computername = computerName

		cursor.execute("SELECT UserPreferenceValue FROM userpreference WHERE UserPreferenceName = 'ComputerName'")
		foundRow = cursor.fetchone()
		foundRow = foundRow[0]
		cursor.execute("UPDATE userpreference SET UserPreferenceValue = '%s' WHERE UserPreferenceName = 'ComputerName'" % (computerName))
		cnx.commit()
		speak("Ok. I will go by the name " + computerName)
		return computerName

	def tellWeather(self):
		answer = 'weather'
		page1 = urllib2.urlopen('https://www.bing.com/search?q=' + answer) 
		html = page1.read()
		WeatherStartPos = 0
		WeatherEndPos = 0
		WeatherStartPos = html.find(' on Bing ')
		WeatherEndPos = html.find('" ',WeatherStartPos)
		BingWeather = html[WeatherStartPos:WeatherEndPos]
		print str("It is %s degrees farenheit%s.") %(BingWeather[13:15],BingWeather[BingWeather.find(","):])
		# raw_input()
		speak(str("It is %s degrees farenheit%s.") %(BingWeather[13:15],BingWeather[BingWeather.find(","):]))
		
	def tellTime(self):
		answer = 'time'
		page1 = urllib2.urlopen('https://www.bing.com/search?q=' + answer) 
		html = page1.read()
		TimeStartPos = 0
		TimeEndPos = 0
		TimeStartPos = html.find('class="b_focusTextLarge">')
		TimeEndPos = html.find('</div>',TimeStartPos)
		BingTime = html[TimeStartPos:TimeEndPos]
		print str(BingTime[25:29])+str(BingTime[32:36])
		speak('It is %s' %str(BingTime[25:29])+str(BingTime[32:36]))
		
	def getInput(self):
		speak('What can I do for  you?')
		try:
			with sr.Microphone() as source:
				print("Listening . . .")
				audio = r.listen(source)
				print("STOP!")
			try:
				answer = r.recognize_google(audio)
			except:
				print("Sorry, but something weird is going on. Please try again later.")
				speak("Sorry, but something weird is going on. Please try again later.")
				return 0
			# answer = answer.replace("'","_")
			return answer
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			speak("Sorry, but I couldn't hear you. You will have to try again.")
			return 0
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
			speak("Sorry, but I can't connect to the Internet right now. Please try again later.")
			return 0
			
	def singleListCheck(self,str):
		queryarray = []
		answerarray = []
		finalstring=''
		for word in str.split():
			queryarray.append("'%"+word+"%'")
		if len(queryarray) == 1:
			rowcount = 0
			query = '''SELECT knownresponse.*,\nSUM((CASE WHEN KnownResponseText LIKE "%s" THEN 1 ELSE 0 END)) AS "Match"\nFROM knownresponse\nGROUP BY KnownResponseNum HAVING Match > 0''' %word
			cursor.execute(query)
			finalstring = cursor.fetchone()
			if finalstring == None:
				return None
			else:
				speak(finalstring[2])
				return 0
			
	def multipleListCheck(self,str):
		i = 0
		tempstring1 = ''
		tempstring2 = ''
		tempstring3 = ''
		querystring = ''
		querystart = "SELECT knownresponse.*,\n"
		queryend = "FROM knownresponse\nGROUP BY KnownResponseNum HAVING Match >= 2"
		array = []
		casearray = []
		finalarray=[]
		reversearray = []
		answerarray = []

		for word in str.split():
			array.append('"%'+word+'%"')
		while i != len(array):
			tempstring1 = array[i]
			if i ==0:
				tempstring2 = " WHEN KnownResponseText LIKE " + tempstring1
			else:
				tempstring2 = tempstring2 +" AND KnownResponseText LIKE " + tempstring1
			i = i + 1
			casearray.append(tempstring2)
		i = 0
		for clause in casearray:
			i = i + 1
			if i == len(casearray):
				clause = "SUM(CASE " + clause + " THEN {}".format(i)
				finalarray.append(clause)
			if i == 1:
				clause = clause + " THEN {} ELSE 0 END) AS 'Match' ".format(i)
				finalarray.append(clause)
			if i != 1 and i != len(casearray):
				clause = clause + " THEN {}\n".format(i)
				finalarray.append(clause)
		i = len(finalarray)
		while i > 0:
			reversearray.append(finalarray[i - 1])
			i = i - 1
		for clause in reversearray:
			querystring = querystring + clause
		querystring = querystart + querystring + queryend
		subquery = 'SELECT IFNULL(B.KnownResponseAnswer,"You Are NULL") KnownResponseAnswer FROM(SELECT Match, KnownResponseAnswer FROM ({})A)B ORDER BY Match DESC'.format(querystring)
		# print subquery
		# raw_input()
		
		i = 0
		finalstring=''
		
		for row in cursor.execute(subquery):
			answerarray.append(row)
			i = i + 1
		
		# raw_input()
		try:
			finalstring = answerarray[0]
			print finalstring[0]
			speak(finalstring[0])
			return 0
		except:
			return None

	def addUnknownResponse(self,str):
		originalstr = str
		try:
			cursor.execute("SELECT UserInputText FROM userinput WHERE UserInputText = '%s'" % str)
			foundRow = cursor.fetchone()
			foundRow = foundRow[0]
			if str == foundRow:
				speak("Sorry. I can't respond to that yet, but I'm working on it.")
		except:
			print "I'm sorry, but I don't know how to respond to that yet."
			speak("I'm sorry, but I don't know how to respond to that yet.")
			
			cursor.execute('''INSERT INTO userinput(UserInputNum,UserInputText) VALUES(?,?)''', (None,str))
			time.sleep(1.5)
			cnx.commit()

			yesno = ''
			speak("Tell me how I can better answer this question for you.")
			
			with sr.Microphone() as source:
				print("Listening . . .")
				audio = r.listen(source)
				print("STOP!")
			try:	
				answer = r.recognize_google(audio)
				# answer = answer.replace("'","_")
				if answer.find('say')==0 or answer.find('so ')==0 or answer.find('SE ')==0 or answer.find('hey')==0 or answer.find('C_est')==0:
					speak("Ok. The next time I respond I will say %s. are you sure this is how you want me to respond?" %answer[4:])
					
					with sr.Microphone() as source:
						print("Listening . . .")
						audio = r.listen(source)
						print("STOP!")
					yesno = r.recognize_google(audio)
					if yesno.find('yes')==0:
						cursor.execute('''INSERT INTO knownresponse(KnownResponseNum,KnownResponseText,KnownResponseAnswer) VALUES(?,?,?)''', (None,str,answer[4:]))
						cnx.commit()
						speak("Ok. I've updated my responses list.")
						return None
					else:
						cursor.execute('''DELETE FROM userinput WHERE userinputnum = (SELECT MAX(userinputnum) FROM userinput)''')
						cnx.commit()
						speak("Ok. you can tell me again later.")
						return None
				else:	
					cursor.execute('SELECT MAX(UserInputNum) FROM userinput')
					fKeyTuple = cursor.fetchone()
					userFKey = fKeyTuple[0]
					cursor.execute('''INSERT INTO learnedresponse(LearnedResponseNum,LearnedResponseText,UserInputNum) VALUES(?,?,?)''', (None,answer,userFKey))
					cnx.commit()
					speak("Thank you. I will work on trying to respond more correct in the future!")
			except sr.UnknownValueError:
				print("Google Speech Recognition could not understand audio")
				speak("Sorry, but I couldn't hear you. You will have to try again.")
				return 0
			except sr.RequestError as e:
				print("Could not request results from Google Speech Recognition service; {0}".format(e))
				speak("Sorry, but I can't connect to the Internet right now. Please try again later.")
				return 0
	
	def news(self):
		response = urllib2.urlopen('http://www.cnn.com/specials/last-50-stories')
		html = response.read()
		count = 0
		startPos = 0
		endPos = 0
		findLinkStartPos = 0
		findLinkEndPos = 0
		print 'Cnn Headlines:'
		for articlefound in html:
			count = count+1

			findLinkStartPos = html.find('contentbox=',findLinkStartPos)
			findLinkEndPos = html.find(' ',findLinkStartPos)
			
			startPos=html.find('cd__headline-text">',startPos)+19
			endPos=html.find("<",startPos)
			
			link=html[findLinkStartPos+12:findLinkEndPos-1]
			article=html[startPos:endPos]
			
			if any(ord(char)>126 for char in article):
			   pass
			else:
				print str(count ) + '. ' + article + '.'
				speak(article)
				
				editedLink = "	- http://www.cnn.com" + link
				
				startPos=endPos
				endPos= endPos + startPos
				
				findLinkStartPos=findLinkEndPos
				findLinkEndPos= findLinkEndPos + findLinkStartPos
				if count >= 5:
					print '\r\n'
					break
		return 0

	def getTestInput(self):
		speak('What can I do for  you?')
		try:
			with sr.Microphone() as source:
				print("Listening . . .")
				audio = r.listen(source)
				print("STOP!")
			answer = r.recognize_google(audio)
			# answer = answer.replace("'","_")
			return answer
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			speak("Sorry, but I couldn't hear you. You will have to try again.")
			return 0
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
			speak("Sorry, but I can't connect to the Internet right now. Please try again later.")
			return 0

	def goodMorning(self):
		self.tellWeather()
		self.tellTime()
		speak("Here are some news headlines")
		self.news()
		return 0

	def rollDice(self,str):
		count = 0
		rollArray = []
		sumOfNum = 0
		

		#if str.find("roll dice") > -1 or str.find("dice") > -1 :
		print str
		str = str.encode("utf8")
		dicePos = str.find("dice")
		numOfDicePos = str[dicePos-3:].find(" ")
		firstSpacePos = str.find(" ")
		try:
			numOfDice = str[firstSpacePos+1:dicePos].strip()

			#numOfDice = numOfDice[0]
			numOfDice = int(w2n.word_to_num(numOfDice))
			if type(numOfDice) == int:
				if numOfDice > 1:
					while count != numOfDice:
						roll = int(randint(1,6))
						rollArray.append(roll)
						count += 1
					for num in rollArray:
						sumOfNum = sumOfNum + num
				if numOfDice == 1:
					print "You rolled a %d" %sumOfNum
					speak("You rolled a %d" %sumOfNum)
				else:
					print "The total is %d" %sumOfNum
					speak("The total is %d" %sumOfNum)
			else:
				print numOfDice
				raw_input()
		except:
			roll = int(randint(1,6))
			print "You rolled a %d" %roll
			speak("You rolled a %d" %roll)
		return 0

	def flipCoin(self):
		coin = randint(0,1)
		if coin == 0:
			speak("It's heads.")
		else:
			speak("It's tails.")
		return 0

	def momJoke(self):
		randSelect = int
		randSelect = cursor.execute('SELECT COUNT(JokeNum) FROM joke')
		randSelect = cursor.fetchone()
		randSelect = randint(1,int(randSelect[0]))
		cursor.execute('SELECT JokeText FROM joke WHERE JokeNum = %d' %randSelect)
		jokeText = cursor.fetchone()
		print jokeText
		speak(jokeText)
		return 0

# computer = Computer('ryan')
# computer.addUnknownResponse("Hey it's me")