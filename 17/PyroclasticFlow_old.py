from itertools import cycle
import numpy as np

def get_data(path):
	with open(path) as file:
		data = list(file.read())

	return data

def get_shapes():
	with open("shapes.txt") as file:
		data = file.read().split("\n\n")

	shape = [np.array([[1 if char=="#" else 0 for char in row] for row in shape.split("\n")]) for shape in data]
	return shape

class CaveMap:
	def __init__(self, shapes, jet_pattern):
		self.cave_map = np.zeros((20, 9))
		self.top_piece_height = 2

		self.shapes = cycle(shapes)
		self.jet_pattern = cycle(jet_pattern)

	@staticmethod
	def __map_to_string(cave_map, top_piece_height):
		string = ""
		for row in reversed(cave_map[:top_piece_height+3, :]):
			string += "".join(["#" if val==1 else "." for val in row]) + "\n"

		return string

	def __str__(self):
		return self.__map_to_string(self.cave_map, self.top_piece_height)

	def add_piece(self):
		# Create piece map (for simple calculations)
		next_piece = next(self.shapes)
		piece_map = np.zeros(self.cave_map.shape)
		piece_bottom = self.top_piece_height+3
		piece_sides = [3, 3+next_piece.shape[1]]
		piece_map[piece_bottom:piece_bottom+next_piece.shape[0], 3:3+next_piece.shape[1]] = next_piece

		# Lower piece
		while piece_bottom > 1 and np.sum(self.cave_map*piece_map)==0:
			# Side-to-side
			jet_char = next(self.jet_pattern)
			# print(jet_char, piece_sides)
			if jet_char == ">" and piece_sides[1] < 8:
				piece_map[:, 1:] = piece_map[:, :-1]
				piece_sides = [side+1 for side in piece_sides]
			elif jet_char == "<" and piece_sides[0] > 1:
				piece_map[:, :-1] = piece_map[:, 1:]
				piece_sides = [side-1 for side in piece_sides]

			piece_map[:-1] = piece_map[1:]
			piece_bottom -= 1

		# Correct piece bottom after collision
		piece_map[1:] = piece_map[:-1]
		piece_bottom += 1

		# Add piece to cave map
		self.cave_map += piece_map
		self.top_piece_height = piece_bottom+next_piece.shape[0]

def part_one():
	jet_pattern = get_data("smallInput.txt")
	shapes = get_shapes()

	cave_map = CaveMap(shapes, jet_pattern)
	# print(cave_map)
	for _ in range(4):
		cave_map.add_piece()
		print(cave_map)

def part_two():
	data = get_data("smallInput.txt")

if __name__ == '__main__':
	part_one()
	# part_two()