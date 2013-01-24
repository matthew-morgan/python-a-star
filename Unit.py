#Unit

class Unit:
	def __init__(self, sprite, faction="Viper"):
		self.sprite = sprite
		self.faction = faction
		self.orderQueue = []
		self.fuel = 30
		self.stable = True #if the stabilizer is damaged the direction of the unit is out of the player's control
		
	def __str__(self):
		return "Unit type: " + repr(self.faction) + " fuel: " + repr(self.fuel)
		