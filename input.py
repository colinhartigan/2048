import getch 

class Input:
	def __init__(self,callback):
		self.listening_for = []
		self.callback = callback

	def bind(self,key):
		self.listening_for.append(key)

	def listen(self):
		while True:
			inp = getch.getch()
			if inp in self.listening_for:
				self.callback(inp)