import pygame
from pygame.locals import *
pygame.init()

white = (255,255,255)
grey = (105,105,105)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,200) 
cyan = (0, 255, 255)
FINDER = 0
MAKER = 1

#screen is a square and dimensions should be a multiple of scale Factor
scaleFactor = 25
screenSize = 700
titleHeight = screenSize/scaleFactor*2


class Tile:
	PATH = 1
	HOLE = 0
	START = -1
	steppedOn = False
	tileX = 0
	tileY = 0
	width = 10
	height = 10
	type = 0 
	
	def __init__(self, x, y, size, path = 0):
		self.tileX = x
		self.tileY = y 
		self.width = size
		self.height = size
		self.type = path
		
	def getCoordinates(self):
		return [self.tileX, self.tileY, self.width, self.height]
		
	def getX(self):
		return self.tileX
		
	def getY(self):
		return self.tileY
		
	def getType(self):
		return self.type
		
	def setType(self, val):
		self.type = val
		
	def stepOn(self):
		self.steppedOn = True
		
	def getSteppedOn(self):
		return self.steppedOn
		
	def mouseOver(self, mouseX, mouseY):
		if mouseX > self.tileX and mouseX < self.width+ self.tileX and mouseY > self.tileY and mouseY < self.height + self.tileY:
			return True
		else:
			return False
			
	def flipType(self, toggle):
		if self.type == self.HOLE:
			self.type = self.PATH
		elif self.type == self.PATH:
			if toggle:
				self.type = self.START
			else:
				self.type = self.HOLE
		elif self.type == self.START:
			if toggle:
				self.type = self.PATH
			else:
				self.type = self.HOLE

class Game:
	FPS = 15
	GAMEOVER = 2
	GAMESTART = 0
	CONTINUE = 1
	screenWidth = 100
	screenHeight = 100
	unitSize = 10
	tiles = []
	level = 0
	gameMode = FINDER
	
	def __init__(self, width = 800, height = 800):
		self.screenWidth = width
		self.screenHeight = height + titleHeight
		self.unitSize = width/scaleFactor
		self.hero = Hero(0, 0+self.unitSize*2, self.screenWidth, scaleFactor)
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont(None, int(self.unitSize*1.5))
		self.gameDisplay = pygame.display.set_mode((self.screenWidth,self.screenHeight))
		self.gameState = Game.GAMESTART
		self.createTiles()
		self.loadTiles(self.level)
				
	def checkInput(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.exitGame()
			if self.gameMode == MAKER:
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse = pygame.mouse.get_pressed()
					if mouse[0]:
						self.flipTiles(False, pygame.mouse.get_pos())
					elif mouse[2]:
						self.flipTiles(True, pygame.mouse.get_pos())
				if event.type == pygame.KEYDOWN:
					if event.key == K_p:
						self.outputTiles()
					if event.key == K_l:
						self.loadTiles(self.level)
			elif self.gameMode == FINDER:
				if event.type == pygame.KEYDOWN:
					if event.key == K_a:
						self.hero.moveLeft()
					elif event.key == K_w:
						self.hero.moveUp()
					elif event.key == K_d:
						self.hero.moveRight()
					elif event.key == K_s:
						self.hero.moveDown()
					elif event.key == K_r:
						self.hero.reset()
						self.gameState = Game.CONTINUE
					elif event.key == K_SPACE:
						self.gameState = Game.CONTINUE
					
	def drawScreen(self):
		#------------------ Title Bar ---------------------#
		self.gameDisplay.fill(black)
		self.messageToScreen("Path Finder", cyan, yOffset = -self.screenHeight/2+self.unitSize)
		
		#----------------- Intro Screen -------------------#
		if self.gameState == Game.GAMESTART:
			self.messageToScreen("Use W,A,S, and D to navigate the path", white, yOffset=-self.unitSize*5)
			self.messageToScreen("Step on each tile of the path to win", white, yOffset=-self.unitSize*4)
			self.messageToScreen("Don't fall off of  the path!", white, yOffset=-self.unitSize*3)
			self.messageToScreen("Press SPACE to begin", white, yOffset=-self.unitSize*2)
		
		#------------------- Game Play --------------------#
		elif self.gameState == Game.CONTINUE:
			self.drawTiles()
			self.drawGrid()
			pygame.draw.rect(self.gameDisplay, green, self.hero.getCoordinates())
		
		#---------------- Game Over Screen ----------------#
		elif self.gameState == Game.GAMEOVER:
			self.messageToScreen("You fell from the path.", red)
			self.messageToScreen("Press R to try again", white, yOffset=self.unitSize)
		#--------------------- Update ---------------------#
		self.checkInput()
		self.gameState = self.checkGameState()
		pygame.display.update()
		self.clock.tick(self.FPS)

		
	def checkGameState(self):
		for tile in self.tiles:
			if self.hero.getX() == tile.getX() and self.hero.getY() == tile.getY():
				if tile.getType() == Tile.PATH:
					tile.stepOn()
					return Game.CONTINUE
				elif tile.getType() == Tile.HOLE:
					self.hero.fall()
					return Game.GAMEOVER
				else:
					return self.gameState
				
		
	def messageToScreen(self, msg, color, xOffset=0, yOffset=0):
		textSurf = self.font.render(msg,True, color)
		textRect = textSurf.get_rect()
		textRect.center = (self.screenWidth/2 + xOffset), (self.screenHeight/2 + yOffset)
		self.gameDisplay.blit(textSurf, textRect)
	
	def createTiles(self):
		for tile in range(scaleFactor*scaleFactor):
			self.tiles.append(Tile((tile%scaleFactor)*self.unitSize, (tile/scaleFactor)*self.unitSize+titleHeight, self.unitSize))
	
	def flipTiles(self, toggle, (mouseX, mouseY)):
		for tile in self.tiles:
			if tile.mouseOver(mouseX, mouseY):
				tile.flipType(toggle)
		
	def drawTiles(self):
		for tile in self.tiles:
			if tile.getType() == Tile.HOLE:
				pygame.draw.rect(self.gameDisplay, black, tile.getCoordinates())
			elif tile.getType() == Tile.PATH:
				pygame.draw.rect(self.gameDisplay, white, tile.getCoordinates())
			elif tile.getType() == Tile.START:
				pygame.draw.rect(self.gameDisplay, blue, tile.getCoordinates())
				
	def loadTiles(self, requestedLevel):
		levelFile = open("level"+str(requestedLevel)+".txt","r")
		types = str.split(levelFile.read(),",")
		for index in range(len(self.tiles)):
			self.tiles[index].setType(int(types[index]))
			if int(types[index]) == Tile.START:
				self.hero.moveToStart(self.tiles[index].getX(), self.tiles[index].getY())
	
	def outputTiles(self):
		levelFile = open("level"+str(self.level)+".txt","w")
		for tile in self.tiles:
			levelFile.write(str(tile.getType())+",")
		levelFile.close()
	
	def drawGrid(self):
		for line in range(scaleFactor):
			pygame.draw.line(self.gameDisplay, grey, (line*screenSize/scaleFactor, titleHeight),(line*screenSize/scaleFactor, screenSize+titleHeight))
			pygame.draw.line(self.gameDisplay, grey, (0, line*screenSize/scaleFactor+titleHeight),(screenSize, line*screenSize/scaleFactor+titleHeight))
		
	def exitGame(self):
		pygame.quit()
		quit()

class Hero:
	startPointX = 0
	startPointY = 0
	
	def __init__(self, startX, startY, screenSize, scale=25):
		self.scaleFactor = scale
		self.heroX = startX
		self.heroY = startY
		self.step = screenSize/self.scaleFactor
		self.heroWidth = screenSize/self.scaleFactor
		self.heroHeight = screenSize/self.scaleFactor
		self.fallen = False
		
	def getCoordinates(self):
		return [self.heroX, self.heroY, self.heroWidth, self.heroHeight]
	
	def getX(self):
		return self.heroX
	
	def getY(self):
		return self.heroY
	
	def moveToStart(self, x, y):
		self.heroX = x
		self.heroY = y 
		self.startPointX = x
		self.startPointY = y 
		
	def reset(self):
		self.heroX = self.startPointX
		self.heroY = self.startPointY
		self.fallen = False
		
	def fall(self):
		self.fallen = True
		
	def moveLeft(self):
		if not self.fallen:
			self.heroX -= self.step
		
	def moveRight(self):
		if not self.fallen:
			self.heroX += self.step
		
	def moveUp(self):
		if not self.fallen:
			self.heroY -= self.step
		
	def moveDown(self):
		if not self.fallen:
			self.heroY += self.step
	
	
pathFinder = Game(screenSize,screenSize)
while True:
	pathFinder.drawScreen()