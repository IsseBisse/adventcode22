from collections import defaultdict
import itertools
import re


def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	elf_coords = [[(x, y) for x, char in enumerate(row) if char == "#"] for y, row in enumerate(data)]
	elf_coords = list(itertools.chain(*elf_coords))

	return elf_coords


def get_adjacent_coords(coord, direction="N"):
	x_current, y_current = coord
	
	if direction == "N":
		offsets = [(-1, -1), (0, -1), (1, -1)]
	
	elif direction == "S":
		offsets = [(-1, 1), (0, 1), (1, 1)]
	
	elif direction == "E":
		offsets = [(1, -1), (1, 0), (1, 1)]
	
	elif direction == "W":
		offsets = [(-1, -1), (-1, 0), (-1, 1)]

	adjacent_coords = [(x_current+x, y_current+y) for x,y in offsets]
	return set(adjacent_coords)


class Elf:
	def __init__(self, coords):
		self.coords = coords
		self.directions = itertools.cycle([("N", (0, -1)), ("S", (0, 1)), ("W", (-1, 0)), ("E", (1, 0))])
		self.proposed_new_coords = None

	def __str__(self):
		return f"Elf at {str(self.coords)}"

	def propose_move(self, elf_coords):
		surrounding_coords = set()
		for direction in ["N", "S", "E", "W"]:
			surrounding_coords = surrounding_coords.union(get_adjacent_coords(self.coords, direction))

		if len(surrounding_coords.intersection(elf_coords)) == 0:
			self.proposed_new_coords = None 
			return None

		test_directions = [next(self.directions) for _ in range(4)]
		for direction, offset in test_directions:
			# direction, offset = next(self.directions)
			adjacent_coords = get_adjacent_coords(self.coords, direction)

			if len(adjacent_coords.intersection(elf_coords)) == 0:
				# print(direction)
				self.proposed_new_coords = tuple(self.coords[axis] + offset[axis] for axis in range(2))
				return tuple(self.coords[axis] + offset[axis] for axis in range(2))


	def move(self, allowed_moves):
		if self.proposed_new_coords is None:
			return

		if self.proposed_new_coords not in allowed_moves:
			return

		self.coords = self.proposed_new_coords


	def update_directions(self):
		# Move starting test direction one step forward
		next(self.directions)
		


def get_elf_limits(elf_coords):
	x_min = min(x for x, _ in elf_coords)
	x_max = max(x for x, _ in elf_coords)
	y_min = min(y for _, y in elf_coords)
	y_max = max(y for _, y in elf_coords)

	return (x_min, x_max), (y_min, y_max)


def plot(elves):
	elf_coords = set(elf.coords for elf in elves)
	x_dim, y_dim = get_elf_limits(elf_coords)
	x_dim = (min(0, x_dim[0]), x_dim[1]+1)
	y_dim = (min(0, y_dim[0]), y_dim[1]+1)

	string = ""
	for y in range(*y_dim):
		for x in range(*x_dim):
			if (x, y) in elf_coords:
				string += "#"

			else:
				string += "."

		string += "\n"

	print(string) 


def calculate_smallest_square(elves):
	elf_coords = set(elf.coords for elf in elves)
	x_dim, y_dim = get_elf_limits(elf_coords)

	tiles = (x_dim[1] - x_dim[0]+1)*(y_dim[1]-y_dim[0]+1)
	empty_tiles = tiles - len(elves)
	return empty_tiles


def get_correct_states():
	with open("correct_states.txt") as file:
		states = file.read().split("\n\n")

	states_dict = dict()
	for state in states:
		rows = state.split("\n")
		num_rounds = int(re.findall(r"[0-9]+", rows[0])[0])
		
		elf_coords = [[(x, y) for x, char in enumerate(row) if char == "#"] for y, row in enumerate(rows[1:])]
		elf_coords = list(itertools.chain(*elf_coords))

		states_dict[num_rounds] = set(elf_coords)

	return states_dict


def part_one():
	elf_coords = get_data("input.txt")
	elves = set()
	for coord in elf_coords:
		elf = Elf(coord)
		elves.add(elf)
	
	correct_states = get_correct_states()
	elf_coords = set(elf.coords for elf in elves)

	num_rounds = 10
	for idx in range(num_rounds):

		elf_coords = set(elf.coords for elf in elves)
		proposed_moves = defaultdict(int)
		for elf in elves:
			# print(elf)
			proposed_coords = elf.propose_move(elf_coords)
			if proposed_coords is not None:
				proposed_moves[proposed_coords] += 1

		allowed_moves = {move for move, count in proposed_moves.items() if count < 2}
		for elf in elves:
			elf.move(allowed_moves)
			elf.update_directions()

		# if idx+1 in correct_states:
		# 	print(f"End of Round {idx+1}")

		# 	elf_coords = set(elf.coords for elf in elves)
		# 	print(correct_states[idx+1].difference(elf_coords))

		# 	plot(elves)

	empty_tiles = calculate_smallest_square(elves)
	print(empty_tiles)
			

def part_two():
	elf_coords = get_data("input.txt")
	elves = set()
	for coord in elf_coords:
		elf = Elf(coord)
		elves.add(elf)
	
	correct_states = get_correct_states()
	elf_coords = set(elf.coords for elf in elves)

	num_rounds = 1
	while True:
	# for _ in range(25):
		elf_coords = set(elf.coords for elf in elves)
		
		proposed_moves = defaultdict(int)
		for elf in elves:
			proposed_coords = elf.propose_move(elf_coords)
			if proposed_coords is not None:
				proposed_moves[proposed_coords] += 1

		if len(proposed_moves) == 0:
			break

		allowed_moves = {move for move, count in proposed_moves.items() if count < 2}
		for elf in elves:
			elf.move(allowed_moves)
			elf.update_directions()

		num_rounds += 1

	print(num_rounds)


if __name__ == '__main__':
	# part_one()
	part_two()