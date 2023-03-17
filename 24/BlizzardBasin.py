from collections import Counter
import itertools


def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	dim = (len(data[0])-2, len(data)-2)
	start = [(x-1, -1) for x, char in enumerate(data[0]) if char == "."][0]
	end = [(x-1, dim[1]) for x, char in enumerate(data[-1]) if char == "."][0]

	blizzards = [[(char, (x-1, y-1)) for x, char in enumerate(row) if char not in [".", "#"]] for y, row in enumerate(data)]
	blizzards = set(itertools.chain(*blizzards))

	return start, end, dim, blizzards

CHAR_TO_DIRECTION = {">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1)}


class Blizzard:
	def __init__(self, char, coords, dim):
		self.coords = list(coords)
		self.direction = CHAR_TO_DIRECTION[char]
		self.dim = dim

	def move(self):
		for axis in range(2):
			self.coords[axis] += self.direction[axis]

			if self.coords[axis] >= self.dim[axis]:
				self.coords[axis] = 0

			elif self.coords[axis] < 0:
				self.coords[axis] = self.dim[axis]-1


def plot(blizzards, dim, position=None):
	blizzard_coords = list(tuple(blizzard.coords) for blizzard in blizzards)
	blizzard_count = Counter(blizzard_coords)

	string = ""
	for y in range(dim[1]):
		for x in range(dim[0]):
			if (x, y) in blizzard_count:
				string += str(blizzard_count[(x, y)])
			else:
				string += "."


		string += "\n"
	print(string)


def possible_next_states(coords, tiles, blizzard_tiles):
	all_next_coords = {tuple(coords[axis] + offset[axis] for axis in range(2)) for offset in [(0, 0), (1, 0), (-1, 0), (0, -1), (0, 1)]}
	tile_allowed_next_coords = all_next_coords.intersection(tiles)
	blizzard_allowed_next_coords = tile_allowed_next_coords.difference(blizzard_tiles)

	return blizzard_allowed_next_coords


def one_round(start, end, tiles, blizzards):
	minute = 0
	states = {start}
	while not end in states:
		print(f"Minute {minute}")
		# print(states)
		blizzard_tiles = set(tuple(blizzard.coords) for blizzard in blizzards)
		# plot(blizzards, dim)

		for blizzard in blizzards:
			blizzard.move()
		blizzard_tiles = set(tuple(blizzard.coords) for blizzard in blizzards)

		next_states = set()
		for state in states:
			next_s = possible_next_states(state, tiles, blizzard_tiles)
			next_states = next_states.union(next_s)

		states = next_states
		minute += 1

	return minute, blizzards


def part_one():
	start, end, dim, blizzard_info = get_data("smallInput.txt")
	blizzards = set()
	for char, coords in blizzard_info:
		blizzards.add(Blizzard(char, coords, dim))

	tiles = {start, end}
	for x in range(dim[0]):
		for y in range(dim[1]):
			tiles.add((x, y))

	minute, _ = one_round(start, end, tiles, blizzards)	
	print(f"Finished after {minute} minutes")


def part_two():
	start, end, dim, blizzard_info = get_data("input.txt")
	blizzards = set()
	for char, coords in blizzard_info:
		blizzards.add(Blizzard(char, coords, dim))

	tiles = {start, end}
	for x in range(dim[0]):
		for y in range(dim[1]):
			tiles.add((x, y))

	minutes = list()
	for start, end in [(start, end), (end, start), (start, end)]:
		minute, _ = one_round(start, end, tiles, blizzards)
		minutes.append(minute)


	print(f"Finished after {sum(minutes)} minutes ({minutes})")


if __name__ == '__main__':
	# part_one()
	part_two()