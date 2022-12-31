import numpy as np
from queue import LifoQueue, PriorityQueue
import random 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from IPython.display import HTML
import math


class Maze:
	def __init__(self, N, S, F):

		"""
		N: integer that indicates the size of the NxN grid of the maze
		S: pair of integers that indicates the coordinates of the starting point (S)
		F: pair of integers that indicates the coordinates of the finish point (F)
		You can add any other parameters you want to customize maze creation (e.g. variables that
		control the creation of additional paths)
		"""

		assert N > 2

		## Make sure start and end are within the grid

		assert S[0] < N-1
		assert S[1] < N-1
		assert F[0] < N-1
		assert F[1] < N-1

		assert S[0] > 0
		assert S[1] > 0
		assert F[0] > 0
		assert F[1] > 0

		# Add here any additional constraints your implementation may have

		self.N = N
		self.S = S
		self.F = F
		self.grid = np.zeros((N, N), dtype=bool)
		stack = LifoQueue()
		visited = set() 

		"""Ένα set που αποθηκεύουμε τα cells που επισκεπτόμαστε. Χρησιμοποιούμε set προκειμένου να τσεκάρουμε 
		αν κάποιο cell ανήκει στο σύνολο σε O(1).
		Η υλοποίηση γίνεται με depth-first search. 
		Αντί για κλήση αναδρομικής συνάρτησης που θα μπορούσε να προκαλέσει stack overflow για πολύ μεγάλες διαστάσεις, 
		χρησιμοποιούμε stack στο οποίο αποθηκεύουμε τους κόμβους που θέλουμε να επισκεφτούμε."""
		
		# Grid initialized with obstacles (array of 0/False)
		# 1/True indicates available neighbours
		
		#"Ενεργοποιούμε" τα κελιά της αρχής και του τέλους ώστε να είναι μέρος του μονοπατιού

		r, c = S
		self.grid[r][c] = 1
		r, c = F
		self.grid[r][c] = 1

		stack.put(self.S)
		visited.add(self.S)

		while not stack.empty():
			x, y = stack.get() #Οι συντεταγμένες του εξεταζόμενου κελιού
			neighbour = []
		
			"""Οι τοίχοι θέλουμε να έχουν πάχος ενός κελιού, συνεπώς θα κοιτάμε τα γειτονικά κελιά (North, South, West, East) 
			που απέχουν δύο κελιά από το εξεταζόμενο κελί. Επιβεβαιώνουμε ότι ο γείτονας αυτός δεν βρίσkεται στην περίμετρο του λαβυρίνθου 
			και ότι δεν τον έχουμε επισκεφτεί και στην συνέχεια τον προσθέτουμε στην λίστα neighbour."""

			if x > 2 and (x - 2, y) not in visited:
				neighbour.append((x - 2, y)) #North
			if x < N - 3 and (x + 2, y) not in visited:
				neighbour.append((x + 2, y)) #South
			if y > 2 and (x, y - 2) not in visited:
				neighbour.append((x, y - 2)) #West
			if y < N - 3 and (x, y + 2) not in visited:
				neighbour.append((x, y + 2)) #East
			
			"""Εφόσον υπάρχει τουλάχιστον ένα γειτονικό κελί στην λίστα neighbour, επιλέγουμε τυχαία ένα και "γκρεμίζουμε" 
			τον τοίχο ανάμεσά στα δύο κελιά (το εξεταζόμενο και τον γείτονά του)"""
			
			if len(neighbour) > 0:
				stack.put((x, y))
				X, Y = random.choice(neighbour) #Οι συντεταγμένες του γείτονα
				
				if X < x:
					self.grid[x - 1][y] = 1 #North
					visited.add((x - 1, y))
				elif X > x:
					self.grid[x + 1][y] = 1 #South
					visited.add((x + 1, y))
				elif Y < y:
					self.grid[x][y - 1] = 1 #West
					visited.add((x, y - 1))
				else:
					self.grid[x][y + 1] = 1 #East
					visited.add((x, y + 1))
	
				self.grid[X][Y] = 1
				visited.add((X, Y))
				stack.put((X, Y))
				
				"""Τέλος, θα έχουμε δημιουργήσει ένα perfect maze (θα έχουμε δηλαδή ένα μονοπατι που θα συνδέει όλα τα κελιά μεταξύ τους).
				Προκειμένου να δημιουργήσουμε πολλαπλά μονοπάτια από την αρχή προς το τέλος πρέπει να  γκρεμίσουμε τουλάχιστον έναν τοίχο (κελί που δεν έχουμε επισκεφτεί).
				Επιλέγουμε τυχαία αυτόν τον τοίχο, με συνθήκη να μην βρίσκεται στην περίμετρο.
				Επιπλέον θέλουμε τα δεξιά και αριστερά κελιά του καθώς και τα πάνω και κάτω να είναι είτε τοίχοι και μονοπάτια αντίστοιχα, είτε μονοπάτια και τοίχοι,
				προκειμένου να μην δημιουργηθεί μονοπάτι πλάτους μεγαλύτερου του ενός κελιού ή μονοπάτι που δεν μπορούμε να έχουμε πρόσβαση."""

		for i in range(self.N//2): #Ο αριθμός που βάλουμε μέσα στο range καθορίζει τον αριθμό των τοίχων που "γκρεμίζονται"
			while (x, y) in visited or not (self.grid[x - 1][y] == self.grid[x + 1][y] and self.grid[x][y - 1] == self.grid[x][y + 1] and self.grid[x + 1][y] != self.grid[x][y - 1]):
				x = random.randrange(1, N - 1)
				y = random.randrange(1, N - 1)
			visited.add((x, y))
			self.grid[x][y] = 1


		
	def draw_map(self, path=None):
		""" Draws the maze as an image. Considers grid values of 0/False to represent obstacles and
		values of 1/True to represent empty cells, but this can be customized. Obstacles are painted
		black and empty cells are painted white. Starting point is painted green and finish point red.
		Optionally accepts as a parameter a path within the maze which is painted blue. 
		"""
		image = np.zeros((self.N, self.N, 3), dtype=int)
		image[~self.grid] = [0, 0, 0]
		image[self.grid] = [255, 255, 255]

		# Uncomment the next 2 lines of code to treat 1/True as obstacles (and 0/False as free maze cells)
		#image[self.grid] = [0, 0, 0]
		#image[~self.grid] = [255, 255, 255]

		image[self.S] = [50, 168, 64]
		image[self.F] = [168, 50, 50]
		if path:
			for n in path[1:-1]:
				image[n] = [66, 221, 245]

		plt.imshow(image)
		plt.xticks([])
		plt.yticks([])
		plt.show()

class Pathfinder:
	def __init__(self, maze, c, h):
		"""
		maze : Αντικείμενο τύπου Maze (από Μέρος 1)
		c : Συνάρτηση που υπολογίζει την πραγματική απόσταση μεταξύ δύο σημείων
		h : Συνάρτηση που υπολογίζει την ευριστική μεταξύ δύο σημείων
		"""
		self.maze = maze
		self.vis = visualization(maze.S, maze.F)
		self.path = []
		self.cost = c
		self.heuristic = h

	### Fill the path list with the coordinates of each point in the path from maze.S to maze.F
	

		"""****		ΘΕΩΡΗΤΙΚΑ	*****"""
	# g(n) = 0 & h(n) = {manhattan(n), euclidean(n)} -> Best First (Θα βρίσκει πάντα λύση εφόσον η ευριστική είναι consistent και admissible) (Οι Manhattan και η euclidean είναι consistent και admissible)
	# g(n) = 1 & h(n) = 0 -> Branch and Bound (θα βρίσκει πάντα βέλτιστη λύση στο πρόβλημά μας (όχι με τον πιο γρήγορο τρόπο όμως))
	# g(n) = 1 & h(n) = {manhattan(n), euclidean(n)} -> A* (Θα βρίσκει πάντα λύση αφού η ευριστική δεν θα υπερεκτιμά την υπολοιπόμενη απόσταση από τον κόμβο στόχο, είναι δηλαδή admissible)
	
	# Άλλες Ευριστικές:
		"""
		1)
		def euclidean_dist_squared(a, b):
			return (a[0] - b[0])**2 + (a[1] - b[1])**2
		2)
		def chebyshev_distance(a, b): #Απόσταση από τον κόμβο στόχο εάν μπορούσαμε να κινηθούμε σε διαγώνιο γειτονικό κελί
			return (abs(a[0] - b[0]) + abs(a[1] - b[1])) - min(abs(a[0] - b[0], a[1] - b[1])
		"""


		"""Δημιουργούμε ένα dictionary (με κλειδιά τις συντεταγμένες των κελιών) για να βρίσκουμε το κόστος (απόσταση από την αφετηρία) ενός κελιού."""

		g_func = {(x, y):-1 for x in range(self.maze.N) for y in range(self.maze.N)}
		g_func[self.maze.S] = 0
		
		# dictionary όπου αποθηκεύουμε τις συντεταγμένες κάθε κελιού που ανήκει στο μονοπάτι-λύση, 
		# θέτοντας ως κλειδί του τις συντεταγμένες του γειτονικού του κελιού (που βρίσκεται πλησιέστερα στο κελί-στόχο)
		solution = {} 
	
		"""Χρησιμοποιούμε priority queue για να δημιουργήσουμε το μέτωπο αναζήτησης (ταξινομημένη ουρά με βάση την τιμή της συνάρτησης κόστους, κατά αύξουσα σειρά)"""
		frontier = PriorityQueue() 
		frontier.put((self.heuristic(self.maze.S, self.maze.F), self.maze.S)) # (f(n), n)

		"""Μέχρι να φτάσουμε τον κόμβο στόχο, βγάζουμε ένα κέλι από την ουρά προτεραιότητας, 
		βρίσκουμε τα γειτονικά κελία-μονοπάτια του και τα προσθέτουμε στην ουρά προτεραιότητας, 
		αφότου υπολογίσουμε την τιμλη της συνάρτησης κόστους τους."""

		while not frontier.empty():
			current_cell = frontier.get()[1]
			if current_cell == self.maze.F:
				break
			x, y = current_cell
			neighbours = []
			if self.maze.grid[x - 1][y] == 1: #North
				neighbours.append((x - 1, y))
			if self.maze.grid[x + 1][y] == 1: #South
				neighbours.append((x + 1, y))
			if self.maze.grid[x][y - 1] == 1: #West
				neighbours.append((x, y - 1))
			if self.maze.grid[x][y + 1] == 1: #East
				neighbours.append((x, y + 1))
			for cell in neighbours:
				if g_func[cell] == -1:
					g_func[cell] = g_func[current_cell] + c(cell, current_cell)
					frontier.put((g_func[current_cell] + c(cell, current_cell) + self.heuristic(cell, self.maze.F), cell))
					solution[cell] = current_cell 
		"""
		Διατρέχουμε το dictionary με τα μονοπάτια και τα αποθηκεύουμε σε μορφή λίστας. 
		Με αυτόν τον τρόπο παίρνουμε το μονοπάτι από τον κόμβο F στο κόμβο S, 
		οπότε στην συνέχεια αντιστρέφουμε την λίστα για να πάρουμε το επιθυμητό αποτέλεσμα
		"""
		i = self.maze.F
		inv_path = [i]
		while i != self.maze.S:
			i = solution[i]
			inv_path.append(i)
		
		self.path = inv_path[::-1]

	def get_path(self):
		return self.path

class visualization:
	def __init__(self, S, F):
		'''
		Η μέθοδος αυτή αρχικοποιεί ένα αντικείμενο τύπου visualization.
		Είσοδος: 
		-> S: το σημείο εκκίνσης της αναζήτησης
		-> F: το σημείο τερματισμού
		'''
		self.S = S
		self.F = F
		self.images = []

	def draw_step(self, grid, frontier, expanded_nodes):
		'''
		Η συνάρτηση αυτή καλείται για να σχεδιαστεί ένα frame στο animation (πρακτικά έπειτα από την επέκταση κάθε κόμβου)
		Είσοδος: 
		-> grid: Ένα χάρτης τύπου grid
		-> frontier: Μια λίστα με τους κόμβους που ανήκουν στο μέτωπο της αναζήτησης
		-> expanded_nodes: Μια λίστα με τους κόμβους που έχουν ήδη επεκταθεί
		Επιστρέφει: None
		Η συνάρτηση αυτή πρέπει να καλεστεί τουλάχιστον μια φορά για να μπορέσει να σχεδιαστει ένα animation (πρεπεί το animation να έχει τουλάχιστον ένα frame).
		'''
		image = np.zeros((grid.N, grid.N, 3), dtype=int)
		image[~grid.grid] = [0, 0, 0]
		image[grid.grid] = [255, 255, 255]
		# Use this to treat 1/True as obstacles
		# image[grid.grid] = [0, 0, 0]
		# image[~grid.grid] = [255, 255, 255]
				
		for node in expanded_nodes:
			image[node] = [0, 0, 128]

		for node in frontier:
			image[node] = [0, 225, 0]

		image[self.S] = [50, 168, 64]
		image[self.F] = [168, 50, 50]
		self.images.append(image)

	def add_path(self, path):
		'''
		Η συνάρτηση αυτή προσθέτει στο τελευταίο frame το βέλτιστο μονοπάτι.
		Είσοδος:
		-> path: Μια λίστα η όποια περιέχει το βέλτιστο μονοπάτι (η οποία πρέπει να περιέχει και τον κόμβο αρχή και τον κόμβο στόχο)
		Έξοδος: None
		'''
		for n in path[1:-1]:
			image = np.copy(self.images[-1])
			image[n] = [66, 221, 245]
			self.images.append(image)
		for _ in range (100):
			self.images.append(image)
			
	def create_gif(self, fps = 30, repeat_delay = 2000):
		if len(self.images) == 0:
			raise EmptyStackOfImages("Error! You have to call 'draw_step' at  first.")
		fig = plt.figure()
		plt.axis('off')
		ims = []
		for img in self.images:
			img = plt.imshow(img)
			ims.append([img])
		ani = animation.ArtistAnimation(fig, ims, interval=1000//fps, blit=True, repeat_delay= repeat_delay)
		plt.close(fig)
		return ani
			
	def save_gif(self, filename, fps = 30):
		'''
		Η συνάρτηση αυτή ξαναδημιουργεί και αποθηκεύει το animation σε ένα αρχείο.
		Είσοδος:
		-> Το όνομα του αρχείου με κατάληξη .gif
		Έξοδος: (None)
		'''
		ani = self.create_gif(fps)
		writer = PillowWriter(fps= fps)
		ani.save(filename, writer=writer)

	def show_gif(self, fps= 30, repeat_delay = 2000):
		'''
		Η συνάρτηση αυτή εμφανίζει inline το animation.
		Είσοδος:
		-> fps: τα frames per second
		Έξοδος: Το αντικείμενο που παίζει το animation
		Exceptions: EmptyStackOfImages αν το animation δεν έχει ούτε ένα frame, δηλαδή αν η draw_step δεν έχει καλεστεί ποτέ.
		'''
		ani = self.create_gif(fps, repeat_delay)
		# return HTML(ani.to_html5_video())
		return HTML(ani.to_jshtml())

	def show_last_frame(self):
		'''
		Η μέθοδος αυτή εμφανίζει inline το τελευταίο frame που έχει δημιουργήθει.
		Είσοδος:
		Έξοδος: Το αντικείμενο που εμφανίζει την εικόνα.
		Exceptions: EmptyStackOfImages αν το animation δεν έχει ούτε ένα frame, δηλαδή αν η draw_step δεν έχει καλεστεί ποτέ.
		'''
		if len(self.images) == 0:
			raise EmptyStackOfImages("Error! You have to call 'draw_step' at  first.")
		else:
			plt.imshow(self.images[-1])


class EmptyStackOfImages(Exception):
	pass

def my_function(a, b):
	#Manhattan distance
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

	#Euclidean distance
	#return (((a[0] - b[0])**2 + (a[1] - b[1])**2)**(1/2))

#for N, S, F in (51, (3, 3), (47, 49)), (25, (3, 7), (23, 19)), (51, (9, 3), (41, 41)):
map = Maze(27, (3, 3), (25, 25))
pf = Pathfinder(maze=map, c = lambda x, y: 1, h = my_function)
map.draw_map(pf.get_path())