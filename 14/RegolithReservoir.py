import itertools
import numpy as np

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [[(int(coord.split(",")[0]), int(coord.split(",")[1])) for coord in row.split(" -> ")] for row in data]

	return data

def draw_line(rock_map, start_coord, end_coord, offset_x):
	start = min(start_coord, end_coord)
	end = max(start_coord, end_coord)

	for x in range(start[0]-offset_x, end[0]-offset_x+1):
		for y in range(start[1], end[1]+1):
			rock_map[x, y] = -1

	return rock_map

class RockMap:
	def __init__(self, rocks, has_floor=False):
		y_max = max([y for x, y in itertools.chain.from_iterable(rocks)])+3
		offset_x = min([x for x, y in itertools.chain.from_iterable(rocks)])
		offset_x = min(500-y_max, offset_x) 	# Bigger offset might if using floor
		x_max = max([x-offset_x for x, y in itertools.chain.from_iterable(rocks)])+1
		x_max = max(x_max, 2*y_max+1)			# Bigger offset might if using floor

		rock_map = np.zeros((x_max, y_max))

		for formation in rocks:
			for idx, start_coord in enumerate(formation[:-1]):
				end_coord = formation[idx+1]
				rock_map = draw_line(rock_map, start_coord, end_coord, offset_x)

		if has_floor:
			rock_map[:, -1] = -1

		self.rock_map = rock_map
		self.offset_x = offset_x

	def __str__(self):
		CHAR_MAP = {-2: "+", -1: "#", 0: ".", 1: "o"}

		string = ""
		for y in range(self.rock_map.shape[1]):
			for x in range(self.rock_map.shape[0]):
				if y == 0 and x+self.offset_x == 500:
					string += "+"
				else:
					string += CHAR_MAP[self.rock_map[x, y]]

			string += "\n"

		return string

	def add_sand(self):
		old_sum = np.sum(self.rock_map)
		while True:
			self.drop_grain_of_sand()

			if np.sum(self.rock_map) == old_sum:
				break

			old_sum = np.sum(self.rock_map)

			# print(self)

		return np.sum(self.rock_map[self.rock_map == 1])

	def drop_grain_of_sand(self):
		grain_x = 500-self.offset_x
		grain_y = 0

		if self.rock_map[grain_x, grain_y] != 0:
			return

		while True:
			if not (0 <= grain_x < self.rock_map.shape[0] and \
				0 <= grain_y < self.rock_map.shape[1]-1):
				return

			if self.rock_map[grain_x, grain_y+1] == 0:
				grain_y += 1

			elif self.rock_map[grain_x-1, grain_y+1] == 0:
				grain_y += 1
				grain_x -= 1

			elif self.rock_map[grain_x+1, grain_y+1] == 0:
				grain_y += 1
				grain_x += 1

			else:
				break

		self.rock_map[grain_x, grain_y] = 1

def part_one():
	rocks = get_data("input.txt")
	rock_map = RockMap(rocks)
	# print(rock_map)

	num_grains_of_sand = rock_map.add_sand()
	print(num_grains_of_sand)
	
def part_two():
	rocks = get_data("input.txt")
	rock_map = RockMap(rocks, has_floor=True)
	# print(rock_map)

	num_grains_of_sand = rock_map.add_sand()
	print(num_grains_of_sand)

if __name__ == '__main__':
	# part_one()
	part_two()