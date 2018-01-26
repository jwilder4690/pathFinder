import pygame
from pygame.locals import *

white = (255,255,255)
grey = (105,105,105)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

#screen is a square and dimensions should be a multiple of scale Factor
scaleFactor = 25
screenSize = 800

class Tile:
	tileX = 0
	tileY = 0
	width = 10
	height = 10
	safePath = 0 
	
	def __init__(self, x, y, size, path = 0):
		self.tileX = x
		self.tileY = y 
		self.width = size
		self.height = size
		self.safePath = path
		
	def getCoordinates(self):
		return [self.tileX, self.tileY, self.width, self.height]
		
	def getPath(self):
		return self.safePath
		
	def setPath(self, val):
		self.safePath = val
		
	def mouseOver(self, mouseX, mouseY):
		if mouseX > self.tileX and mouseX < self.width+ self.tileX and mouseY > self.tileY and mouseY < self.height + self.tileY:
			return True
		else:
			return False
			
	def flipType(self):
		if self.safePath == 0:
			self.safePath = 1
		else:
			self.safePath = 0
		
		
			
class Game:
	FPS = 15
	startX = 0
	startY = 0
	screenWidth = 100
	screenHeight = 100
	unitSize = 10
	tiles = []
	level = 0
	
	def __init__(self, width = 800, height = 800):
		self.screenWidth = width
		self.screenHeight = height
		self.unitSize = width/scaleFactor
		self.clock = pygame.time.Clock()
		self.gameDisplay = pygame.display.set_mode((self.screenWidth,self.screenHeight))
		self.createTiles()

	
	def checkInput(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.exitGame()
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.flipTiles(pygame.mouse.get_pos())
			if event.type == pygame.KEYDOWN:
				if event.key == K_p:
					self.outputTiles()
				if event.key == K_l:
					self.loadTiles(self.level)
					
					
	def drawScreen(self):
		self.checkInput()
		self.gameDisplay.fill(black)
		self.drawTiles()
		self.drawGrid()
		pygame.display.update()
		self.clock.tick(self.FPS)

	def createTiles(self):
		for tile in range(scaleFactor*scaleFactor):
			self.tiles.append(Tile((tile%scaleFactor)*self.unitSize, (tile/scaleFactor)*self.unitSize, self.unitSize))
	
	def flipTiles(self, (mouseX, mouseY)):
		for tile in self.tiles:
			if tile.mouseOver(mouseX, mouseY):
				tile.flipType()
		
	def drawTiles(self):
		for tile in self.tiles:
			if tile.getPath() == 1:
				pygame.draw.rect(self.gameDisplay, white, tile.getCoordinates())
			else:
				pygame.draw.rect(self.gameDisplay, black, tile.getCoordinates())
				
	def loadTiles(self, requestedLevel):
		levelFile = open("level"+str(requestedLevel)+".txt","r")
		bools = str.split(levelFile.read(),",")
		for index in range(len(self.tiles)):
			self.tiles[index].setPath(int(bools[index]))
			print self.tiles[index].getPath()
		#for tile,bool in zip(self.tiles, bools):
			#tile.setPath(bool)
		#for tile2 in self.tiles:
			#print tile2.getPath()
	
	def outputTiles(self):
		#self.level += 1
		levelFile = open("level"+str(self.level)+".txt","w")
		for tile in self.tiles:
			levelFile.write(str(tile.getPath())+",")
		levelFile.close()
	
	def drawGrid(self):
		for line in range(scaleFactor):
			pygame.draw.line(self.gameDisplay, grey, (line*screenSize/scaleFactor, 0),(line*screenSize/scaleFactor, screenSize))
			pygame.draw.line(self.gameDisplay, grey, (0, line*screenSize/scaleFactor),(screenSize, line*screenSize/scaleFactor))
		
	def exitGame(self):
		pygame.quit()
		quit()
		
pathMaker = Game(screenSize,screenSize)
while True:
	pathMaker.drawScreen()