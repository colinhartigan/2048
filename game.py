from termcolor import colored
from replit import clear
import random
from input import Input

class Game:
	def __init__(self):
		self.grid_size = 100
		self.board = [[0 for i in range(self.grid_size)] for j in range(self.grid_size)]

		self.row_width = 7
		self.row_height = 3
		self.num_colors = {
			0: "white",
			2: "red",
			4: "yellow",
			8: "green",
			16: "blue",
			32: "magenta",
			64: "cyan",
			128: "white",
			256: "red",
			512: "yellow",
			1024: "green",
			2048: "blue",
			4096: "magenta",
			8192: "cyan",
		}
		self.num_attrs = {
			0: ["concealed"],
			2: [],
			4: [],
			8: [],
			16: [],
			32: [],
			64: [],
			128: ["bold"],
			256: ["bold"],
			512: ["bold"],
			1024: ["bold"],
			2048: ["bold"],
			4096: ["bold"],
			8192: ["bold"],
		}
		self.directions = {
			"w":1,
			"a":4,
			"s":3,
			"d":2,
		}

		#bind keys
		self.input = Input(self.keyboard_listen) 
		self.input.bind("w")
		self.input.bind("a")
		self.input.bind("s")
		self.input.bind("d")


		# start the game
		self.generate_tile()
		self.generate_tile()
		self.input.listen()

	def check_legal_move(self,direc):
		filled_squares = []

		invalids = 0

		for i in range(0,self.grid_size): 
			for j in range(0,self.grid_size): 
				if self.board[i][j] != 0:
					filled_squares.append((i,j))

		for i in filled_squares:
			movement = self.check_adjacent(direc,i[0],i[1])
			if movement == 0:
				invalids += 1

		if invalids == len(filled_squares):
			return False
		else:
			return True

	def check_adjacent(self,direc,row,col):
		'''
		returns an int describing allowed movement
		possible values for each entry: 
			0 - cannot move anymore in this direction
			1 - can move in this direction 
			2 - can move in this direction/combine
		'''

		val = self.board[row][col] 

		if ((row - 1) == -1 and (direc == 1)) or ((row + 1) == self.grid_size and (direc == 3)) or ((col - 1) == -1 and (direc == 4)) or ((col + 1) == self.grid_size and (direc == 2)):
			return 0

		adj = self.board[row-1 if direc == 1 else row+1 if direc == 3 else row][col+1 if direc == 2 else col-1 if direc == 4 else col]
		if val == adj:
			return 2 
		if adj == 0:
			return 1
		else:
			return 0
		
	def move(self,direc):
		'''
		directions:
			1 - up
			2 - right
			3 - down 
			4 - left
		'''
		if not self.check_legal_move(direc):
			count = 0
			for i in range(1,4):
				if not self.check_legal_move(i):
					count += 1
			if count == 4:
				print("game over lmao")
				exit()
			else:
				return
		moves = 1
		
		already_combined = [[0 for i in range(self.grid_size)] for j in range(self.grid_size)]

		while moves != -1:
			row = range(0,self.grid_size) if direc == 1 else range(self.grid_size-1,-1,-1) if direc == 3 else range(0,self.grid_size)
			col = range(0,self.grid_size) if direc == 4 else range(self.grid_size-1,-1,-1) if direc == 2 else range(0,self.grid_size)
			moves = 0
			for i in row: 
				for j in col: 
					if self.board[i][j] != 0:
						new_row = i-1 if direc == 1 else i+1 if direc == 3 else i
						new_col = j+1 if direc == 2 else j-1 if direc == 4 else j

						movement = self.check_adjacent(direc,i,j)

						if movement == 1:
							moves += 1
							self.board[new_row][new_col] = self.board[i][j]
							self.board[i][j] = 0
						if movement == 2 and already_combined[i][j] != 1:
							moves += 1
							self.board[new_row][new_col] = self.board[i][j] + self.board[new_row][new_col]
							self.board[i][j] = 0
							already_combined[new_row][new_col] = 1
			if moves == 0:
				moves = -1
		self.generate_tile()


	def keyboard_listen(self, key):
		self.move(self.directions[key])


	# tile generation --------------------------------------------------
	def find_blank_squares(self):
		# find blank tiles
		blanks = []
		for i, v in enumerate(self.board):
			for j, g in enumerate(v):
				if g == 0:
					blanks.append((i, j))
		return blanks

	def generate_tile(self):
		# generate a new tile
		blanks = self.find_blank_squares()
		if blanks == []:
			print('game over lmao')
			
		selected = random.randrange(len(blanks))
		probability = random.randrange(1,3)
		self.board[blanks[selected][0]][blanks[selected][1]] = 2 if probability == 1 else 4
		self.draw_board()
	# ------------------------------------------------------------------


	# draw board ------------------------------------------------------
	def draw_board(self):
		clear()

		horiz_divider = f"|{'-' * ((self.row_width*self.grid_size)+(self.grid_size-1))}|"

		board = horiz_divider + ''.join(self.__make_row(v, last=True if i == self.grid_size-1 else False) for i, v in enumerate(self.board)) + horiz_divider

		print(board)

	def __make_row(self, nums, last=False):
		horiz_divider = f"|{'-'*(self.row_width)}" * self.grid_size + "|"

		row = f"| {' '*(self.row_width-1)}" * self.grid_size + "|"

		num_row = ''.join(self.__make_number_square(i) for i in nums)

		board = f"\n{row}" * ((self.row_height // 2) - 1 if self.row_height % 2 == 0 else(self.row_height // 2)) + f"\n|{num_row}" + f"\n{row}" * (self.row_height // 2) + f"\n{horiz_divider if not last else ''}"

		return board

	def __make_number_square(self, inp):
		num = colored(inp, self.num_colors[inp], attrs=self.num_attrs[inp])
		num_len = len(str(inp))
		mid_width = (self.row_width - num_len) // 2

		num = f"{' '*mid_width}{num}{' '*mid_width if (self.row_width % 2 == 0 and (num_len % 2 == 0)) or (self.row_width % 2 == 1 and (num_len % 2 == 1)) else ' '*(mid_width+1)}|"

		return num
	# ------------------------------------------------------------------



