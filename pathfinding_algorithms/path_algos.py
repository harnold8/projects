import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH+180, WIDTH))
pygame.display.set_caption("Search Algorithms")

#some color codes
RED = (28,  103, 193)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
EFFECTCOLOR = (97, 159, 232)



#node structure for the grid (x,y). every node is connected with maximum 4 neighbors. stored in neighbors
#diagonal connections are not allowed.
#a spot also holds a color for the visualization
class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		#unaccessed color = white
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows
		#the color might changes after a certain step interval
		self.time_effekt = 0

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	#after 7 steps, change the color
	def make_closed(self):
		self.color = RED
		self.time_effekt = 7

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def check_barrier(self):
		if self.color == BLACK:
			return True

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = YELLOW

	def draw(self, win):
		#change the color after a certain step interval
		if self.time_effekt > 0 and self.is_closed():
			pygame.draw.rect(win, EFFECTCOLOR, (self.x, self.y, self.width, self.width))
			self.time_effekt += -1
		else:
			pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	#assigns all the possible neighbors (max:D,U,R,L), barriers for example are not allowed to be a neighbor
	def update_neighbors(self, grid):
		self.neighbors = []
		#             can still move down          is not a barrier
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])
		#(0,0) is the upper right corner
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])
		# number of rows=number of columns
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

#manhattan distance
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

#draws the shortest path for A*, Greedy BFS and DIJK
def reconstruct_path(came_from, start, current, draw):
	while current in came_from:
		current = came_from[current]
		if current != start:
			current.make_path()
		draw()

#draws the shortest path for bfs
def draw_path(draw, shortest_path, start, end):
	for items in shortest_path:
		if items != start and items != end:
			items.color = YELLOW
	draw()

# finds shortest path between 2 nodes of a graph using BFS
def bfs(draw, grid, start, end):
	# keep track of explored nodes
	explored = []
	# keep track of all the paths to be checked
	queue = [[start]]

	# keeps looping until all possible paths have been checked
	while queue:
		# pop the first path from the queue
		path = queue.pop(0)
		# get the last node from the path
		node = path[len(path)-1]

		if node not in explored:
			neighbours = node.neighbors
			# go through all neighbour nodes and build a new path
			# if it was never visited, mark it for the visualization
			for neighbour in neighbours:
				if neighbour.color == WHITE:
					neighbour.make_closed()
				new_path = list(path)
				#append the new element to the existing path
				new_path.append(neighbour)
				queue.append(new_path)

				if neighbour == end:
					#return new_path
					draw_path(draw, new_path, start, end)
					return None
			# mark node as explored
			explored.append(node)
		draw()


#eucledian distance, was used for test purposes
def eucl(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return math.sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))

#A* algo
def algorithm(draw, grid, start, end):
	#to get a tie braker for equal fs
	count = 0
	#to get the min element
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	#dictionary to assign nodes to nodes to create the shortest path
	came_from = {}
	#setting g and f scores to inf at the beginning, except for the start pos
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	#manhattan dist
	f_score[start] = h(start.get_pos(), end.get_pos())
	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		#get the minimum val node
		current = open_set.get()[2]
		open_set_hash.remove(current)
		#shortest path found
		if current == end:
			reconstruct_path(came_from, start, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			#updating the g_score for the neighbors
			temp_g_score = g_score[current] + 1
			#if a neighbor has a new lower value, save the new val
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				#manhattan dist + steps
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
		draw()
		if current != start:
			current.make_closed()
	return False

#dij
def dijk(draw, grid, start, end):
	#to get a tie braker for equal fs
	count = 0
	#to get the min element
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	#dictionary to assign nodes to nodes to create the shortest path
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		#get the minimum val node
		current = open_set.get()[2]
		open_set_hash.remove(current)
		#shortest path found
		if current == end:
			reconstruct_path(came_from, start, end, draw)
			end.make_end()
			return True
		#if a neighbor has a new lower val, save it
		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((g_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
		draw()
		if current != start:
			current.make_closed()

	return False

#Greedy best first search, with manhattan dist
def greedy(draw, grid, start, end):
	#to get the min element, x value as tie braker
	open_set = PriorityQueue()
	open_set.put((0, start.get_pos()[1], start))
	#dictionary to assign nodes to nodes to create the shortest path
	came_from = {}
	#heuristic, manhattan dist
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())
	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		#get the minimum val node
		current = open_set.get()[2]
		open_set_hash.remove(current)
		#shortest path found
		if current == end:
			reconstruct_path(came_from, start, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
				#add neighbor to the stack, if it hasn't been visited yet
				if neighbor not in open_set_hash and not neighbor.is_closed():
					# calculate the heuristics for the neighbors
					f_score[neighbor] = h(neighbor.get_pos(), end.get_pos())
					if current != start:
						came_from[neighbor] = current
					open_set.put((f_score[neighbor], neighbor.get_pos()[1], neighbor))
					open_set_hash.add(neighbor)
		draw()

		if current != start:
			current.make_closed()

	return False

#data structure for the grid
def make_grid(rows, width):
	grid = []
	#how large a button is going to be
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)
	return grid

#draw the grid lines
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		#drawing horizontal lines    x1     y1      x2      y2
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows+1):
			# drawing vert lines          x1     y1      x2      y2
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

#drawing a text at pos x,y
def draw_text(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)

#drawing the buttons for the algo selection
def draw_button(win, rows, width, text, font, color, y):
	DARKBLUE = [0, 8, 78]
	LBLUE = [0, 19, 195]
	row_width = width / rows
	#outer rectangle
	pygame.draw.rect(win, DARKBLUE, (width + 2, y, row_width * 11, row_width * 3.5))
	#inner
	pygame.draw.rect(win, LBLUE, (width + 7, y+5, row_width * 11 - 10, row_width * 3.5 - 10))
	textcolor = WHITE
	#if selected color = Yellow
	if color:
		textcolor = YELLOW
	draw_text(text, font, textcolor, win, width + 12, y+20)

#a faster drawing algo for the search algorithms, to only update the grid structure
def draw(win, grid, rows, width):
	for row in grid:
		for spot in row:
			# drawing the rectangles
			spot.draw(win)
	# drawing the grid
	draw_grid(win, rows, width)
	pygame.display.update()

#drawing visualization with the menu
def draw2(win, grid, rows, width, colorMatrix):
	#initializing every window in white
	win.fill(WHITE)
	for row in grid:
		for spot in row:
			#drawing the rectangles
			spot.draw(win)
	#drawing the grid
	draw_grid(win, rows, width)
	#selecting font
	pygame.font.init()
	font = pygame.font.Font('freesansbold.ttf', 20)

	#drawing the left mouse icon
	mouseImg = pygame.image.load('mouse_button.png')
	scaled = pygame.transform.scale(mouseImg, (50, 60))
	WIN.blit(scaled, (width + 2, 0))
	draw_text('draw/select', font, BLACK, win, width + 55, 30)

	#drawing the right mouse icon
	mouseImg = pygame.image.load('right_button.png')
	scaled = pygame.transform.scale(mouseImg, (50, 60))
	WIN.blit(scaled, (width + 2, 70))
	draw_text('delete', font, BLACK, win, width + 55, 100)

	#the spacebar
	spacebar = pygame.image.load('spacebar.jpg')
	scaled = pygame.transform.scale(spacebar, (80, 30))
	WIN.blit(scaled, (width + 2, 150))
	draw_text('run', font, BLACK, win, width + 90, 155)

	#key c
	key_c = pygame.image.load('key_c.png')
	scaled = pygame.transform.scale(key_c, (50, 50))
	WIN.blit(scaled, (width + 2, 190))
	draw_text('reset grid', font, BLACK, win, width + 55, 205)

	#drawing the buttons for the algo selection
	buttonNames = ["A*", "Greedy BFS", "DIJK", "BFS"]
	buttonPos = 250
	for i,name in enumerate(buttonNames):
		draw_button(win, rows, width, name, font, colorMatrix[i], buttonPos)
		#60 is the height of a button
		buttonPos += 60

	pygame.display.update()



#getting the node that we clicked at
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos
	row = y // gap
	col = x // gap
	return row, col

def main(win, width):
	#matrix for button selection
	colorMatrix = [0, 0, 0, 0]
	#number of cubes/nodes
	ROWS = 50
	grid = make_grid(ROWS, width)
	start = None
	end = None
	run = True
	draw2(win, grid, ROWS, width, colorMatrix)

	while run:
		#checking for user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT

				#where we pressed
				pos = pygame.mouse.get_pos()

				limits = grid[0][0].total_rows * grid[0][0].width

				if pos[0] > limits:
					#Button/Algo selection
					#resetting the value
					if 250 < pos[1] < 490:
						for i in range(4):
							colorMatrix[i] = 0
					#setting new value
					if 250 < pos[1] < 310:
						#A*
						colorMatrix[0] = 1
					elif  310 < pos[1] < 370:
						#Greedy
						colorMatrix[1] = 1
					elif 370 < pos[1] < 430:
						#DJK
						colorMatrix[2] = 1
					elif 430 < pos[1] < 490:
						# BFS
						colorMatrix[3] = 1
					draw2(win, grid, ROWS, width, colorMatrix)
				#A position within the grid was selected
				else:
					row, col = get_clicked_pos(pos, ROWS, width)
					spot = grid[row][col]
					#assigning start node
					if not start and spot != end:
						start = spot
						start.make_start()
					#assigning end node
					elif not end and spot != start:
						end = spot
						end.make_end()
					#drawing barriers
					elif spot != end and spot != start:
						spot.make_barrier()

				draw(win, grid, ROWS, width)

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				#delete nodes with a right click
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

				draw(win, grid, ROWS, width)

			if event.type == pygame.KEYDOWN:
				#spacebar = run the algo
				if event.key == pygame.K_SPACE and start and end:
					#determine which algo was selected
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					algo = -1
					for i,value in enumerate(colorMatrix):
						if value:
							algo = i
							break;
					if algo == 0:
						algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
					elif algo == 1:
						greedy(lambda: draw(win, grid, ROWS, width), grid, start, end)
					elif algo == 2:
						dijk(lambda: draw(win, grid, ROWS, width), grid, start, end)
					elif algo == 3:
						bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
					else:
						None
					draw(win, grid, ROWS, width)

					#resetting the algo colors afterwards
					for i in range(ROWS):
						for j in range(ROWS):
							if not grid[i][j].is_barrier() and grid[i][j] != start and grid[i][j] != end:
								grid[i][j].color = WHITE

				#deleting the grid on key press "c"
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
					draw(win, grid, ROWS, width)

	pygame.quit()

main(WIN, WIDTH)