from okcomputer import aiEngine
import os, time, sys
from random import randint
import msvcrt

os.system('mode con: cols=35 lines=15')

def delay(float):
	time.sleep(float)

def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

def robeFace():
	while True:

		clearScreen()

		print '''
	------\     /------ 
	*******     *******
	*     *     *     *
	*  *  *     *  *  *
	*     *     *     *
	*******     *******
	         ^
	        ^^^
	       ^^^^^
	     _________
	    /_________\\
	    \_________/
		'''
		if msvcrt.kbhit():
			if ord(msvcrt.getch()) > 0:
				msvcrt.getch()
				aiEngine()

		else:
			delay(randint(0,4))
		clearScreen()

		print '''
	------\     /------ 
	*******     *******
	*******     *******
	** * **     ** * **
	*     *     *     *
	*******    *******
	         ^
	        ^^^
	       ^^^^^
	     _________
	    /_________\\
	    \_________/ 
		'''

		clearScreen()
		
		print '''
	------\     /------ 
	*******     *******
	*******     *******
	*******     *******
	*     *     *     *
	*******     *******
	         ^
	        ^^^
	       ^^^^^
	     _________
	    /_________\\
	    \_________/ 
		'''
		
		clearScreen()

		print '''
	------\     /------ 
	*******     *******
	*******     *******
	*******     *******
	*******     *******
	*******     *******
	         ^
	        ^^^
	       ^^^^^
	     _________
	    /_________\\
	    \_________/ 
		'''

		clearScreen()

		print '''
	------\     /------ 
	*******     *******
	*******     *******
	*******     *******
	*     *     *     *
	*******     *******
	         ^
	        ^^^
	       ^^^^^
	     _________
	    /_________\\
	    \_________/ 
		'''
		
		clearScreen()		

		print '''
	------\     /------ 
	*******     *******
	*******     *******
	** * **     ** * **
	*     *     *     *
	*******     *******
	         ^
	        ^^^
	       ^^^^^
	     _________
	    /_________\\
	    \_________/ 
		'''

		clearScreen()
if __name__ == '__main__':
	robeFace()