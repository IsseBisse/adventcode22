import re

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [[int(item) for item in re.findall(r"[\-0-9]+", row)] for row in data]

	return data

class Sensor:
	def __init__(self, sensor_pos, beacon_pos):
		self.x, self.y = sensor_pos
		self.beacon_x, self.beacon_y = beacon_pos

		self.manhattan_radius = abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y) 

	def __str__(self):
		return f"Sensor at x: {self.x}, y: {self.y}. Manhattan distance to beacon: {self.manhattan_radius}"

	def seen_positions(self, y):
		x_distance = self.manhattan_radius - abs(self.y - y)
		if x_distance < 0:
			return []

		return list(range(self.x-x_distance, self.x+x_distance+1))

	def seen_range(self, y):
		x_distance = self.manhattan_radius - abs(self.y - y)
		if x_distance < 0:
			return []

		return (self.x-x_distance, self.x+x_distance+1)

def part_one():
	data = get_data("input.txt")
	
	sensors = list()
	known_items = list()
	for x, y, beacon_x, beacon_y in data:
		sensors.append(Sensor((x, y), (beacon_x, beacon_y)))
		known_items.append((beacon_x, beacon_y))
		known_items.append((x, y))

	known_items = set(known_items)

	seen_positions = list()
	y = 2000000
	for sensor in sensors:
		seen_positions += sensor.seen_positions(y)

	known_items_at_row = set(beacon[0] for beacon in known_items if beacon[1] == y)
	impossible_positions = set(seen_positions).difference(known_items_at_row)

	# print(impossible_positions)
	print(len(impossible_positions))

def overlaps(first, second):
	(first_start, first_end), (second_start, second_end) = first, second
	return (first_end >= second_start and first_start <= second_end) or \
		(second_end >= first_start and second_start <= first_end)

def covers_row(ranges, limit):
	ranges = sorted(ranges)
	first = ranges[0]
	for second in ranges[1:]:
		if overlaps(first, second):
			first = (min(first[0], second[0]), max(first[1], second[1]))

		else:
			return False

	return first[0] <= limit[0] and first[1] >= limit[1]

def part_two():
	data = get_data("input.txt")
	
	sensors = list()
	for x, y, beacon_x, beacon_y in data:
		sensors.append(Sensor((x, y), (beacon_x, beacon_y)))

	possible_positions = list()
	limit = 4000001
	allowed_positions = set(range(limit))
	for y in range(limit):
		seen_ranges = list()
		for sensor in sensors:
			sensor_range = sensor.seen_range(y)
			if sensor_range:
				seen_ranges.append(sensor_range)

		if not covers_row(seen_ranges, (0, limit-1)):
			seen_positions = list()
			for low, high in seen_ranges:
				seen_positions += list(range(low, high))

			seen_positions = set(seen_positions)
			for x in range(limit):
				if x not in seen_positions:
					possible_positions.append((x, y))

	print(possible_positions)
	print(possible_positions[0]*4000000 + possible_positions[1])

if __name__ == '__main__':
	# part_one()
	# part_two()
