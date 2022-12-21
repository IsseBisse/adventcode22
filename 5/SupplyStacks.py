import re

def get_data(path):
	with open(path) as file:
		stacks, rearrangement = tuple(file.read().split("\n\n"))

	stack_rows = stacks.split("\n")
	stacks = {i+1: list() for i in range(len(re.findall(r"[0-9]+", stack_rows[-1])))}
	for row in stack_rows[:-1]:
		for idx, char in enumerate(row[1::4]):
			if char != " ":
				stacks[idx+1].append(char)

	rearrangement = [tuple([int(value) for value in re.findall(r"[0-9]+", row)]) for row in rearrangement.split("\n")]

	return stacks, rearrangement

def move_single(stacks, from_, to):
	stacks[to].insert(0, stacks[from_].pop(0))
	return stacks

def move(stacks, amount, from_, to):
	for _ in range(amount):
		stacks = move_single(stacks, from_, to)

	return stacks

def part_one():
	stacks, rearrangement = get_data("input.txt")

	# print(stacks)
	for amount, from_, to in rearrangement:
		# print(f"{amount} from {from_} to {to}")
		stacks = move(stacks, amount, from_, to)
		# print(stacks)

	top_of_stack = "".join([stacks[key][0] for key in stacks])
	print(top_of_stack)

def move_multiple(stacks, amount, from_, to):
	move_crates = list()
	for _ in range(amount):
		move_crates.append(stacks[from_].pop(0))

	for crate in move_crates[::-1]:
		stacks[to].insert(0, crate)

	return stacks

def part_two():
	stacks, rearrangement = get_data("input.txt")

	# print(stacks)
	for amount, from_, to in rearrangement:
		# print(f"{amount} from {from_} to {to}")
		stacks = move_multiple(stacks, amount, from_, to)
		# print(stacks)

	top_of_stack = "".join([stacks[key][0] for key in stacks])
	print(top_of_stack)

if __name__ == '__main__':
	# part_one()
	part_two()