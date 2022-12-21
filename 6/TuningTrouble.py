from collections import deque

def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def find_start_idx(message, maxlen):
	start = deque(maxlen=maxlen)

	for idx, char in enumerate(message):
		start.append(char)

		if len(set(start)) == maxlen:
			return idx+1

def part_one():
	message = get_data("input.txt")
	print(find_start_idx(message, 4))

def part_two():
	message = get_data("input.txt")
	print(find_start_idx(message, 14))

if __name__ == '__main__':
	part_one()
	part_two()