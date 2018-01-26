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
	safePath = False
	
	def __init__(self, x, y, size, path = False):
		self.tileX = x
		self.tileY = y 
		self.width = size
		self.height = size
		self.safePath = path
		
	def getCoordinates(self):
		return [self.tileX, self.tileY, self.width, self.height]
	

class Game:
	FPS = 15
	startX = 0
	startY = 0
	screenWidth = 100
	screenHeight = 100
	unitSize = 10
	tiles = []
	
	def __init__(self, width = 800, height = 800):
		self.screenWidth = width
		self.screenHeight = height
		self.unitSize = width/scaleFactor
		self.clock = pygame.time.Clock()
		self.gameDisplay = pygame.display.set_mode((self.screenWidth,self.screenHeight))
		for tile in range(scaleFactor*scaleFactor):
			self.tiles.append(Tile((tile%scaleFactor)*self.unitSize, (tile/scaleFactor)*self.unitSize, self.unitSize))
	
	def checkInput(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.exitGame()

					
	def drawScreen(self):
		self.checkInput()
		self.gameDisplay.fill(black)
		self.drawTiles()
		self.drawGrid()
		pygame.display.update()
		self.clock.tick(self.FPS)
		
	def drawTiles(self):
		for tile in self.tiles:
			pygame.draw.rect(self.gameDisplay, red, tile.getCoordinates())
	
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