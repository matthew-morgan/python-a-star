#Grid
from Cell import Cell

class Grid:
	""" Contains a list of Cell objects """
	#hexTransforms = [(-1,0), (1,0), (0,-1), (0,1), (-1, -1), (1, 1)]
	#hexTransforms = [(-1,0), (1,0), (0,-1), (0,1), (1, -1), (-1, -1)]
	#hexTransforms = [(-2,1), (-1,1), (1,2), (2,1),(1,-1),(-1,2)]
	oddTransforms = [(0,-1), (0,1), (-1,0), (1, 1), (1,0), (-1,1)] 
	evenTransforms  = [(0,-1), (0,1), (-1,0), (-1,-1), (1,0), (1,-1)]
	
	def __init__(self, gridWidth, gridHeight):
			self.gridWidth = gridWidth
			self.gridHeight = gridHeight
			self.CellDict = {}
			for i in xrange(self.gridWidth):
				for j in xrange(self.gridHeight):
					self.CellDict[(i,j)] = Cell(i,j)
					
			self.units = []
	
	def addUnit(self, coords, sprite, faction=None):
		self.CellDict[coords].addUnit(sprite)
		self.units.append(self.CellDict[coords].unit)
		
	
	def areConnected(self, cell1, cell2): #Obsolete for the  time being, might have a use in the future. Also borked now.
		return ((cell1.horizontal_coordinate - cell2.horizontal_coordinate), (cell1.vertical_coordinate - cell2.vertical_coordinate)) \
		in self.hexTransforms	

	def allConnected(self, cell):
		connected = []
		if cell.horizontal_coordinate % 2 == 0:
			hexTransforms = self.evenTransforms
		else: hexTransforms = self.oddTransforms
		for transform in hexTransforms:
			xTransform = cell.horizontal_coordinate + transform[0]
			yTransform = cell.vertical_coordinate + transform[1]
			if xTransform >= 0 and xTransform < self.gridWidth and  yTransform >= 0 and yTransform < self.gridHeight:
				neighbour = self.CellDict[(xTransform, yTransform)]
				if neighbour.isWalkable():
					connected.append(neighbour)
		return connected

	def connectedCellCost(self, cell1, cell2):
		return 10

	def heuristic(self, cell1, cell2): 
		dx = (cell1.horizontal_coordinate - cell2.horizontal_coordinate)
		dy = (cell1.vertical_coordinate - cell2.vertical_coordinate)
		d = dx - dy
		return 10 * max(abs(dx), abs(dy), abs(d))
		
	def calculateG(self, cell):
		G = 0
		while cell.parent != None:
			G += self.connectedCellCost(cell, cell.parent)
			cell = cell.parent
		return G
	
	def compareFcosts(self, cell1, cell2):
		if cell1.fCost > cell2.fCost: return 1
		if cell1.fCost < cell2.fCost: return -1
		if cell1.fCost == cell2.fCost: return 0
	
	def findPath(self, startCell, endCell):
		openList = [startCell]
		closedList = []
		startCell.gCost = self.calculateG(startCell)
		startCell.hCost = self.heuristic(startCell, endCell)
		startCell.fCost = startCell.gCost + startCell.hCost
		while endCell not in closedList and openList: #Checking the endcell not being in the openList makes the algorithm faster than checking for it in the closedList but is not always optimal
				openList.sort(self.compareFcosts)
				currentCell = openList[0]	
				closedList.append(currentCell)
				openList.remove(currentCell)
				for cell in self.allConnected(currentCell):
						if cell not in closedList:
							if cell not in openList:
								cell.gCost = self.calculateG(cell)
								cell.hCost = self.heuristic(cell, endCell) #Factorise out this stuff
								cell.fCost = cell.gCost + cell.hCost
								cell.parent = currentCell
								openList.append(cell)
							if cell in openList and self.calculateG(currentCell) + self.connectedCellCost(cell, currentCell) < cell.gCost:
								cell.parent = currentCell
								cell.gCost = self.calculateG(cell)
								cell.hCost = self.heuristic(cell, endCell)
								cell.fCost = cell.gCost + cell.hCost
		path = [endCell]
		p = endCell.parent
		while p != None:
			path.append(p)
			p = p.parent
		path.reverse()
		return path
						
