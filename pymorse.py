#-----------------#
#-- PYMORSE ------#
#-- by Cardboard -#
#-- v0.01 --------#
#-- 12312012 -----#
#-----------------#

import pygame, sys
from pygame.locals import *
pygame.init()

class Pymorse:
	def __init__(self):
		self.message = ''
		self.startChar = 0
		self.endChar = 0
		self.startPause = 0
		self.wordEnd = True
		self.color = (255, 0, 0)
		self.curMorse = '' # holds dits and dahs for current letter
		self.curChar = '' # holds letter to be added to message
		self.morseList = [ ('a', '.-'), ('b', '-...'), ('c', '-.-.'),
				('d', '-..'), ('e', '.'), ('f', '..-.'), ('g', '--.'),
				('h', '....'), ('i', '..'), ('j', '.---'), ('k', '-.-'),
				('l', '.-..'), ('m', '--'), ('n', '-.'), ('o', '---'),
				('p', '.--.'), ('q', '--.-'), ('r', '.-.'), ('s', '...'),
				('t', '-'), ('u', '..-'), ('v', '...-'), ('w', '.--'),
				('x', '-..-'), ('y', '-.--'), ('z', '--..')]

		self.key = pygame.K_SPACE # key used to tap
		self.pressed = False
		self.delay_dit = 200 # anything longer than this is a dah
		self.delay_endChar = 500
		self.delay_pause = 2000
		
	def press(self, TIME):
		if self.keys[self.key]:
			if self.pressed == False:
				self.startChar = TIME
				self.color = (0, 255, 0)
				self.wordEnd = False
				self.pressed = True
	def release(self, TIME):
		if not(self.keys[self.key]):
			if self.pressed == True:
				self.endChar = TIME
				self.startPause = TIME
				self.color = (255, 0, 0)
				self.pressed = False
	def calculateChar(self, TIME):
		delay_pressRelease = self.endChar - self.startChar
		delay_releasePress = TIME - self.startPause
		if self.pressed == False: # if key pressed
			if delay_pressRelease <= self.delay_dit and delay_pressRelease != 0: # delay = dit
				self.curMorse += '.'
				self.startChar = 0
				self.endChar = 0
				self.startPause = TIME
			elif delay_pressRelease > self.delay_dit: # delay = dah
				self.curMorse += '-'
				self.startChar = 0
				self.endChar = 0
				self.startPause = TIME
			if delay_releasePress > self.delay_pause and self.wordEnd == False:
				self.message += ' '
				self.color = (0, 128, 255)
				self.wordEnd = True
			# delay is long enough to start new character but not long enough for a space
			if delay_releasePress > self.delay_endChar and delay_releasePress < self.delay_pause:
				for letter, morse in self.morseList:
					if self.curMorse == morse:
						self.curChar = letter
				self.message += self.curChar
				# RESET VARIABLES TO RECEIVE NEXT LETTER
				self.curChar = ''
				self.curMorse = ''
	#			self.startPause = 0
				self.color = (0, 0, 255)

	def check(self, TIME):
		self.keys = pygame.key.get_pressed()
		self.press(TIME)
		self.release(TIME)
		self.calculateChar(TIME)


pymorse = Pymorse()
surface = pygame.display.set_mode((320, 320))

font = pygame.font.Font(None, 50)

while True:
	surface.fill((255,255,255))
	pygame.draw.rect(surface, pymorse.color, (0,150,320,170))
	
	message = pymorse.curMorse
	text = font.render(message, 0, (0,0,255))
	surface.blit(text, (0,0))
	message = pymorse.message
	text = font.render(message, 0, (0,0,255))
	surface.blit(text, (0,55))	

	pygame.display.update() 
	time = pygame.time.get_ticks()

	pymorse.check(time)

	for event in pygame.event.get():
		if event.type == QUIT:
			print('SHUTTING DOWN...')
			pygame.quit()
			sys.exit()
	if pymorse.keys[pygame.K_ESCAPE]:
		print('SHUTTING DOWN...')
		pygame.quit()
		sys.exit()
