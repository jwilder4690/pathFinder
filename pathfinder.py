import pygame
from pygame.locals import *

#screen is a square and dimensions should be a multiple of scale Factor
scaleFactor = 25
screenSize = 800

class Game:
	FPS = 15
	startX = 0
	startY = 0
	white = (255,255,255)
	grey = (105,105,105)
	black = (0,0,0)
	red = (255,0,0)
	green = (0,255,0)
	screenWidth = 100
	screenHeight = 100
	
	def __init__(self, width = 800, height = 800):
		self.screenWidth = width
		self.screenHeight = height
		self.hero = Hero(self.startX, self.startY, self.screenWidth, scaleFactor)
		self.clock = pygame.time.Clock()
		self.gameDisplay = pygame.display.set_mode((self.screenWidth,self.screenHeight))
	
	def checkInput(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.exitGame()
			if event.type == pygame.KEYDOWN:
				if event.key == K_a:
					self.hero.moveLeft()
				if event.key == K_w:
					self.hero.moveUp()
				if event.key == K_d:
					self.hero.moveRight()
				if event.key == K_s:
					self.hero.moveDown()
					
	def drawScreen(self):
		self.checkInput()
		self.gameDisplay.fill(self.black)
		self.drawGrid()
		pygame.draw.rect(self.gameDisplay, self.green, self.hero.getCoordinates())
		pygame.display.update()
		self.clock.tick(self.FPS)
		
	def drawGrid(self):
		for line in range(scaleFactor):
			pygame.draw.line(self.gameDisplay, self.grey, (line*screenSize/scaleFactor, 0),(line*screenSize/scaleFactor, screenSize))
			pygame.draw.line(self.gameDisplay, self.grey, (0, line*screenSize/scaleFactor),(screenSize, line*screenSize/scaleFactor))
		
	def exitGame(self):
		pygame.quit()
		quit()

class Hero:
		
	def __init__(self, startX, startY, screenSize, scale=25):
		self.scaleFactor = scale
		self.heroX = startX
		self.heroY = startY
		self.step = screenSize/self.scaleFactor
		self.heroWidth = screenSize/self.scaleFactor
		self.heroHeight = screenSize/self.scaleFactor
		
	def getCoordinates(self):
		return [self.heroX, self.heroY, self.heroWidth, self.heroHeight]
		
	def moveLeft(self):
		self.heroX -= self.step
		
	def moveRight(self):
		self.heroX += self.step
		
	def moveUp(self):
		self.heroY -= self.step
		
	def moveDown(self):
		self.heroY += self.step
	
	
pathFinder = Game(screenSize,screenSize)
while True:
	pathFinder.drawScreen()