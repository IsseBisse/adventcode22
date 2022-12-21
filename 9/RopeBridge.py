def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [tuple(row.split(" ")) for row in data]
	data = [(direction, int(length)) for direction, length in data]

	return data

class Rope:
	DIRECTION_TO_COORDS = {"U": (0, 1), "D": (0, -1), "R": (1, 0), "L": (-1, 0)}

	def __init__(self):
		self.head = [0, 0]
		self.tail = [0, 0]

		self.tail_previous = [tuple(self.tail)]

	def __str__(self):
		return f"H:{self.head}, T{self.tail}"

	def print_tail_path(self):
		for row_idx in range(5):
			for col_idx in range(6):
				if (col_idx, 4-row_idx) in self.tail_previous:
					print("# ", end="")
				else:
					print(". ", end="")
			print("")

	def move(self, direction, length):
		direction_coords = self.DIRECTION_TO_COORDS[direction]
		for _ in range(length):
			self.head = [self.head[i] + direction_coords[i] for i in range(2)]
			self.update_tail()

			# print(self)

	def update_tail(self):
		head_tail_xy_distance = [self.head[i] - self.tail[i] for i in range(2)]
		head_tail_euclidian_distance = sum([axis_difference**2 for axis_difference in head_tail_xy_distance])
		if head_tail_euclidian_distance > 2:
			head_tail_difference = [-int(axis_difference/abs(axis_difference)) \
				if abs(axis_difference) == max([abs(distance) for distance in head_tail_xy_distance]) else 0 \
				for axis_difference in head_tail_xy_distance]

			self.tail = [self.head[i] + head_tail_difference[i] for i in range(2)]
			self.tail_previous.append(tuple(self.tail))

def part_one():
	data = get_data("input.txt")

	rope = Rope()
	for direction, length in data:
		rope.move(direction, length)
		# print(rope)

	# rope.print_tail_path()
	print(len(set(rope.tail_previous)))

class Knot:
	DIRECTION_TO_COORDS = {"U": (0, 1), "D": (0, -1), "R": (1, 0), "L": (-1, 0)}

	def __init__(self, name):
		self.name = name
		self.pos = [0, 0]
		self.previous_pos = list(tuple(self.pos))
		self.tail = None

	def __str__(self):
		string = f"{self.name}: {self.pos}"
		if self.tail is not None:
			string += f", {str(self.tail)}"

		return string

	def move(self, direction, length):
		direction_coords = self.DIRECTION_TO_COORDS[direction]
		for _ in range(length):
			self.pos = [self.pos[i] + direction_coords[i] for i in range(2)]
			self.tail.follow(self.pos)

	def follow(self, head_pos):
		head_self_xy_distance = [head_pos[i] - self.pos[i] for i in range(2)]
		head_self_euclidian_distance = sum([axis_difference**2 for axis_difference in head_self_xy_distance])
		if head_self_euclidian_distance > 2:
			head_self_difference = [-int(axis_difference/abs(axis_difference)) \
				if abs(axis_difference) == max([abs(distance) for distance in head_self_xy_distance]) else 0 \
				for axis_difference in head_self_xy_distance]

			self.pos = [head_pos[i] + head_self_difference[i] for i in range(2)]
			self.previous_pos.append(tuple(self.pos))

		if self.tail is not None:
			self.tail.follow(self.pos)


def part_two():
	# data = get_data("smallInput.txt")
	# data = get_data("largerInput.txt")
	data = get_data("input.txt")

	head = Knot("H")
	curr = head
	for idx in range(9):
		next_ = Knot(f"{idx+1}")
		curr.tail = next_
		curr = next_

	for direction, length in data:
		head.move(direction, length)
		print(head)

	curr = head
	while curr.tail is not None:
		curr = curr.tail

	print(len(set(curr.previous_pos)))


if __name__ == '__main__':
	part_one()
	part_two()