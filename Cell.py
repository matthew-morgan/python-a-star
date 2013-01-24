#Cell
from Unit import Unit
class Cell:
	def __init__(self, horizontal_coordinate, vertical_coordinate, walkable=True):
		self.horizontal_coordinate = horizontal_coordinate
		self.vertical_coordinate = vertical_coordinate
		self.walkable = walkable
		self.selected = False
		
	def __str__(self):
		return "Cell x: " + repr(self.horizontal_coordinate) + " y: " + repr(self.vertical_coordinate)
	def isWalkable(self):
		return self.walkable
	
	parent = None # Used by A*
	screenCoordinates = None
	baseImg = None
	unit = None
	
	def addUnit(self, sprite, faction=None):
		self.unit = Unit(sprite)
		self.unit.sprite.x = self.screenCoordinates[0] #This will prolly have to be changed for animation
		self.unit.sprite.y = self.screenCoordinates[1]
		self.walkable = False
		
	def getUnit(self):
		return self.unit
		
		
	def deleteUnit(self):
		self.unit = None
		self.walkable = True
		
	def setSelected(self):
		self.selected = True
		self.baseImg.color = (100,100,100) #todo: make a dict of colours
	
	def hilight(self):
		self.baseImg.color = (100,100,100)
	def unHilight(self):
		self.baseImg.color = (255,255,255)