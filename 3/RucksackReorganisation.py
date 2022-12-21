def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

LETTER_TO_PRIO = {chr(i+97): i+1 for i in range(26)} | {chr(i+65): i+27 for i in range(26)}

def shared_item_score(rucksack):
	num_items = len(rucksack) // 2
	first, second = rucksack[:num_items], rucksack[num_items:]

	shared_item = list(set(first).intersection(set(second)))
	return LETTER_TO_PRIO[shared_item[0]]

def part_one():
	rucksacks = get_data("input.txt")

	scores = map(shared_item_score, rucksacks)
	print(sum(scores))

def group_shared_item_score(group):
	shared = set(group[0])
	for rucksack in group[1:]:
		shared = shared.intersection(rucksack)

	shared = list(shared)[0]
	return LETTER_TO_PRIO[shared]

def part_two():
	rucksacks = get_data("input.txt")
	
	groups = [[rucksacks[start+i] for i in range(3)] for start in range(0, len(rucksacks), 3)]
	scores = map(group_shared_item_score, groups)
	print(sum(scores)) 

if __name__ == '__main__':
	part_one()
	part_two()