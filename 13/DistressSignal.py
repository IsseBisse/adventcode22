from functools import cmp_to_key
from itertools import chain

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n\n")

	data = [(eval(row.split("\n")[0]), eval(row.split("\n")[1])) for row in data]

	return data

# def comp_int(left, right):
# 	if left == right:
# 		return 0
# 	elif left < right:
# 		return 1
# 	elif left > right:
# 		return -1

# def comp_list(left_list, right_list):
# 	idx = 0
# 	while True:

# def comp_values(left, right):
# 	# Return -1 (incorrect order), 0 (continue) or 1 (correct order)
# 	if isinstance(left, int) and isinstance(right, int):
# 		return comp_int(left, right)

# 	else:
# 		left = [left] if not isinstance(left, int) else left
# 		right = [right] if not isinstance(right, int) else right


# class Packet(list):
# 	def __init__(self, iterable):
# 		for i, obj in enumerate(iterable):
# 			super().__init__(Packet(item) if isinstance(item, list) else item for item in iterable)

# 	def is_right_order(self, other):
# 		for first, second in zip(self, other):
# 			print(first, second)
# 			if isinstance(first, int) and isinstance(second, int):
# 				if first > second:
# 					return False

# 				continue

# 			else:
# 				first = Packet()

def is_right_order(left, right):
	for idx in range(max(len(left), len(right))):
		if idx == len(left):
			return True
		
		elif idx == len(right):
			return False

		else:
			first = left[idx]
			second = right[idx]
	
		# print(first, second)

		if isinstance(first, int) and isinstance(second, int):
			if first == second:
				continue

			else:
				return first < second

		else:
			first = first if isinstance(first, list) else [first]
			second = second if isinstance(second, list) else [second]

			right_order = is_right_order(first, second)
			if right_order is None:
				continue

			else:
				return right_order

	return None


def part_one():
	pairs = get_data("input.txt")

	right_order_sum = 0
	for idx, (left, right) in enumerate(pairs):
		print(left, right)
		if is_right_order(left, right):
			right_order_sum += idx+1
		# print(idx, is_right_order(left, right))
		# print()
		
	print(right_order_sum)
	
def compare(first, second):
	right_order = is_right_order(first, second)
	if right_order is None:
		return 0

	else:
		return 1 if right_order else -1

def part_two():
	pairs = get_data("input.txt")
	items = list(chain(*pairs))
	
	# Divider packets
	dividers = [[[2]], [[6]]]
	items += dividers

	items = sorted(items, key=cmp_to_key(compare), reverse=True)
	# for item in items:
	# 	print(item)

	divider_idx = [items.index(div)+1 for div in dividers]
	print(divider_idx[0]*divider_idx[1])

if __name__ == '__main__':
	# part_one()
	part_two()