from Grid import Grid
from HexView import HexView
import pyglet
from pyglet.gl import *
import os
from pyglet.window import mouse
#import profile

class Game():
	def __init__(self, window):
		self.window = window
		self.colours = {'white' : (255, 255, 255, 0), 'outerspace': (65, 74, 76, 0) }
		pyglet.gl.glClearColor(*self.colours['outerspace'])
		
		#Load images, create batch-groups, a batch
		pyglet.resource.path = ['tiles']
		pyglet.resource.reindex()
		#self.explosion_stream = open('explosion2strip.png', 'rb')
		#self.explosion = pyglet.image.load('explosion1strip.png')
		self.hexWater = pyglet.resource.image('hex.png')
		self.hexMud = pyglet.resource.image('hexDirt.png')
		self.hexUnwalkable = pyglet.resource.image('hexUnwalkable.png')
		self.ship = pyglet.resource.image('ship.png')
		self.background = pyglet.graphics.OrderedGroup(0)
		self.foreground = pyglet.graphics.OrderedGroup(1)
		self.effectslayer = pyglet.graphics.OrderedGroup(2)
		self.cellbatch = pyglet.graphics.Batch()
		
		self.grid = Grid(12, 8)	
		
		self.hexView = HexView(self.grid, 64, 55, 17, 0, 0) #todo: something to get this centered in the screen automatically
		self.screenCoordinates = self.hexView.screenCoordinates()
		
		self.selectedCell = None
		self.phase = 1
		self.movingUnit = False #True if a unit is being moved
		self.currentFaction = "Viper"
		
		#self.exp_seq = pyglet.image.ImageGrid(self.explosion, 1, 32)
		#self.boom = pyglet.image.Animation.from_image_sequence(self.exp_seq, 0.09) 
		#self.boomsprite = pyglet.sprite.Sprite(self.boom, x=10, y=10, batch=self.cellbatch, group=self.foreground)
	
	def initializeCellSprites(self): # use iteritems and refactor this nonsense
		for cell in self.grid.CellDict.iterkeys():
			if not self.grid.CellDict[cell].walkable: self.grid.CellDict[cell].baseImg = pyglet.sprite.Sprite(self.hexUnwalkable, x=self.grid.CellDict[cell].screenCoordinates[0], y=self.grid.CellDict[cell].screenCoordinates[1], batch=self.cellbatch, group=self.background)
			else: self.grid.CellDict[cell].baseImg = pyglet.sprite.Sprite(self.hexWater, x=self.grid.CellDict[cell].screenCoordinates[0], y=self.grid.CellDict[cell].screenCoordinates[1], batch=self.cellbatch, group=self.background)
		
	
	def initializeUnits(self):
		self.grid.addUnit((3,3), pyglet.sprite.Sprite(self.ship, batch=self.cellbatch, group=self.foreground), faction = "Viper")
		self.grid.addUnit((3,4), pyglet.sprite.Sprite(self.ship, batch=self.cellbatch, group=self.foreground), faction = "Viper")
		self.grid.addUnit((5,3), pyglet.sprite.Sprite(self.ship, batch=self.cellbatch, group=self.foreground), faction = "Raider")
		self.grid.addUnit((2,3), pyglet.sprite.Sprite(self.ship, batch=self.cellbatch, group=self.foreground), faction = "Raider")
		
		
	def on_draw(self):
		glEnable(GL_BLEND) 
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 
		self.window.clear()
		self.cellbatch.draw()
		#self.boomsprite.draw()
		#pyglet.clock.ClockDisplay().draw()
	
	def validCell(self, coords):
		return coords in self.grid.CellDict #Should this be here?
		
	def on_mouse_motion(self,x, y, dx, dy):
		pass

	def moveUnit(self, startCell, endCell):
		path = self.grid.findPath(startCell, endCell)
		startCell.unit.path = path
		for cell in path: print cell
		self.movingUnit = False
	
	def resolveMove(self):
		for unit in self.grid.units:
			print unit 
	
	def on_mouse_press(self, x, y, button, modifiers):
		coords = self.hexView.getClickedCell(x,y) 
		if self.validCell(coords):
			cell = self.grid.CellDict[coords]
			if not self.movingUnit and cell.unit != None:
				if cell.unit.faction == self.currentFaction:
					self.movingUnit = True
					self.currentCell = cell
					print cell.unit
					return	
					
			if self.movingUnit and cell != None:
				self.moveUnit(self.currentCell, cell)
		if button == mouse.RIGHT:
			self.resolveMove()
			
	def startGame(self):
		self.initializeCellSprites()
		self.initializeUnits()
		self.window.on_draw = self.on_draw
		self.window.on_mouse_press = self.on_mouse_press
		self.window.on_mouse_motion = self.on_mouse_motion
		#self.window.event(self.on_draw)
		#self.window.event(self.on_mouse_press)
		pyglet.app.run()
		

def Main():
	window = pyglet.window.Window()
	game = Game(window)
	game.startGame()

#if __name__ == '__main__': profile.run('Main()')
if __name__ == '__main__': Main()
	

