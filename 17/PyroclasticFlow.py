from dataclasses import dataclass
from itertools import cycle
from typing import List
from tqdm import tqdm

def get_data(path):
	with open(path) as file:
		data = list(file.read())

	jets = [1 if char == ">" else -1 for char in data]

	return jets

def get_shapes():
	shapes = [[(0,0), (1,0), (2,0), (3,0)],
			  [(1,0), (0,1), (1,1), (2,1), (1,2)],
			  [(0,0), (1,0), (2,0), (2,1), (2,2)],
			  [(0,0), (0,1), (0,2), (0,3)],
			  [(0,0), (1,0), (0,1), (1,1)]]
	
	return shapes


def add_direction(coord, direction):
	return tuple(axis+step for axis, step in zip(coord, direction))

@dataclass
class Rock:
	coords: List[int]
	x_min: int = 0
	x_max: int = 6

	def move(self, direction):
		x_coords = [x for x, _ in self.coords]
		if min(x_coords) == self.x_min and direction[0] < 0:
			return

		if max(x_coords) == self.x_max and direction[0] > 0:
			return

		for idx, coord in enumerate(self.coords):
			self.coords[idx] = add_direction(coord, direction)

	def room_to_move(self, direction, seated_rocks):
		drop_rock = Rock([coord for coord in self.coords])
		drop_rock.move(direction)
		drop_rock_coords = set(drop_rock.coords)
		return len(drop_rock_coords.intersection(seated_rocks)) == 0

	def is_above(self, peaks):
		return all(y > peaks[x] for x,y in self.coords)


class Cave:
	def __init__(self, rocks, jets):
		self.rocks = cycle(rocks)
		self.jets = cycle(jets)
		self.width = 7
		self.seated_rock_coords = set((x, -1) for x in range(self.width))

	def __str__(self):
		string = ""

		y_max = max([y for _, y in self.seated_rock_coords]) + 3

		for row in reversed(range(y_max)):
			for col in range(7):
				char = "#" if (col, row) in self.seated_rock_coords else "."
				string += char

			string += "\n"

		return string

	def peak_heights(self):
		height = [-1] * self.width
		for x, y in self.seated_rock_coords:
			height[x] = max(height[x], y)

		return height 

	def drop(self, rock, peaks):
		while True:
			next_horizontal_direction = next(self.jets)
			if rock.room_to_move((next_horizontal_direction, 0), self.seated_rock_coords):
				rock.move((next_horizontal_direction, 0))
			
			if rock.room_to_move((0, -1), self.seated_rock_coords):
				rock.move((0, -1))	
			else:
				return rock

			# print(rock)

	def one_turn(self):
		peaks = self.peak_heights()
		highest_peak = max(peaks)
		rock = Rock([coord for coord in next(self.rocks).coords])
		rock.move((2, highest_peak+4))
		# print("start: " + str(rock))

		rock = self.drop(rock, peaks)
		self.seated_rock_coords = self.seated_rock_coords.union(set(rock.coords))


def part_one():
	rock_coords = get_shapes()
	rocks = [Rock(coords) for coords in rock_coords]
	jets = get_data("input.txt")
	cave = Cave(rocks, jets)

	for idx in range(2022):
		cave.one_turn()
		# print(max(cave.peak_heights()))
		# print(cave)
		# print(idx, flush=True)

	print(max(cave.peak_heights()) + 1)
	# print(cave.seated_rock_coords)


def principal_period(s):
    i = (s+s).find(s, 1, -1)
    return None if i == -1 else s[:i]

def part_two():
	rock_coords = get_shapes()
	rocks = [Rock(coords) for coords in rock_coords]
	jets = get_data("input.txt")
	cave = Cave(rocks, jets)
	
	peak_height_difference = list()
	previous_peak_height = 0
	for idx in range(4000):
		cave.one_turn()
		max_peak_height = max(cave.peak_heights())
		peak_height_difference.append(max_peak_height-previous_peak_height)
		previous_peak_height = max_peak_height

	difference_string = "".join([str(num) for num in peak_height_difference])
	for start, _ in enumerate(difference_string):
		period = principal_period(difference_string[start:])
		if period is not None:
			break

	# print(difference_string)
	# print(period)

	num_rocks = 1000000000000
	period_digits = [int(char) for char in period]
	height = sum(peak_height_difference[:start]) + \
			 (num_rocks - start) // len(period) * sum(period_digits) + \
			 sum(period_digits[:(num_rocks - start) % len(period)]) + 1
	print(height)

if __name__ == '__main__':
	part_one()
	part_two()