import math
class HexView:
	def __init__(self, grid, tileWidth, tileHeight, xOffset, xStart, yStart):
		self.grid = grid
		self.tileHeight = tileHeight
		self.tileWidth = tileWidth
		self.xOffset = xOffset
		self.xStart = xStart
		self.yStart = yStart
		self.cellsWide = grid.gridWidth
		self.cellsHight = grid.gridHeight
		
	def screenCoordinates(self):
		screenCoordinates = []
		for cell in self.grid.CellDict.iterkeys():
			if self.grid.CellDict[cell].horizontal_coordinate == 0:
				screenX = 0
				screenY = self.grid.CellDict[cell].vertical_coordinate * self.tileHeight
			elif self.grid.CellDict[cell].horizontal_coordinate % 2 == 1:
				screenX = (self.grid.CellDict[cell].horizontal_coordinate * (self.tileWidth - self.xOffset))
				screenY = (self.grid.CellDict[cell].vertical_coordinate * self.tileHeight) + (self.tileWidth / 2) -4 #Don't ask...
			else:
				screenX = (self.grid.CellDict[cell].horizontal_coordinate * (self.tileWidth - self.xOffset)) 
				screenY = (self.grid.CellDict[cell].vertical_coordinate * self.tileHeight)
			self.grid.CellDict[cell].screenCoordinates = ((screenX + self.xStart, screenY + self.yStart))
			
	def getClickedCell(self, clickedX, clickedY): #might be misnamed. does not return a cell but coordinates that need to be checked for validity. also you don't have to click
		# http://www-cs-students.stanford.edu/~amitp/Articles/GridToHex.html
		# if the tile size changes diagonal will have to be changed too. The x'th element is the y coordinate of the diagonal line.
		diagonal = [[17, 16, 15, 15, 14, 14, 13, 12, 12, 11, 11, 10, 9, 9, 8, 7, 7, 6, 6, 5, 4, 4, 3, 2, 2, 1, 1, 0],[0, 1, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8, 9, 9, 10, 11, 11, 12, 12, 13, 14, 14, 15, 15, 16, 17]]
		clickedX -= self.xStart
		clickedY -= (self.yStart + 4) 
		row = clickedY / (self.tileHeight / 2)
		col = clickedX / (self.tileWidth - self.xOffset)
		if clickedX % (self.tileWidth - self.xOffset) < self.xOffset:
			if diagonal[(row + col)%2][clickedY%(self.tileHeight / 2)] >= clickedX % (self.tileWidth - self.xOffset): 		
				col -= 1		
		return (col, (row-(col %2))/2)
		
		