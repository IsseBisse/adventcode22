from collections import Counter
from tqdm import tqdm

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [eval(row) for row in data]

	return data

def get_offset_cubes(cube, offsets):
	sides = list()
	for idx in range(3):
		for offset in offsets:
			side = [coord for coord in cube]
			side[idx] += offset
			sides.append(tuple(side))
			
	return sides

def part_one():
	cubes = get_data("input.txt")

	sides = list()
	for cube in cubes:
		sides += get_offset_cubes(cube, [-0.5, 0.5])
		
	exposed_sides = [side for side, count in Counter(sides).items() if count == 1]
	print(len(exposed_sides))

# Wrong! Doesn't work on connected enclosed spaces
# def is_enclosed_noncube(cube, cubes):
# 	surrounding_cubes = get_offset_cubes(cube, [-1, 1])
# 	if cube in cubes:
# 		return False

# 	for cube in surrounding_cubes:
# 		if cube not in cubes:
# 			return False

# 	return True

def enclosed_volume(cube, cubes):
	surrounding_cubes = get_offset_cubes(cube, [-1, 1])
	cubes = cubes.copy()
	cubes.append(cube)

	enclosed_cubes = [cube]
	for cube in surrounding_cubes:
		if cube not in cubes:
			enclosed_cubes += enclosed_volume(cube, cubes)

	return enclosed_cubes

def is_enclosed_noncube(cube, cubes):
	try:
		enclosed_cubes = enclosed_volume(cube, cubes)
	except RecursionError as e:
		return None

	return enclosed_cubes


def get_enclosed_cubes(cubes):
	axis_coords = list(zip(*cubes))

	all_enclosed_cubes = list()
	for x in tqdm(range(min(axis_coords[0]), max(axis_coords[0])+1), position=0):
		for y in tqdm(range(min(axis_coords[1]), max(axis_coords[1])+1), position=1, leave=False):
			for z in range(min(axis_coords[2]), max(axis_coords[2])+1):
				cube = (x, y, z)
				if cube in cubes or cube in all_enclosed_cubes:
					continue

				enclosed_cubes = is_enclosed_noncube(cube, cubes)
				if enclosed_cubes is not None:
					all_enclosed_cubes += enclosed_cubes 

	all_enclosed_cubes = list(set(all_enclosed_cubes))
	return all_enclosed_cubes
	
def get_test_data():
	cubes = list()
	for x in range(1, 4):
		for y in range(1, 5):
			for z in range(1, 5):
				cube = (x, y, z)
				if cube not in [(2, 2, 2), (2, 2, 3), (2, 3, 2)]:
					cubes.append(cube)

	return cubes

def part_two():
	import sys
	sys.setrecursionlimit(400)
	# cubes = get_test_data()
	cubes = get_data("input.txt")
	sides = list()
	for cube in cubes:
		sides += get_offset_cubes(cube, [-0.5, 0.5])
		
	sides = [side for side, count in Counter(sides).items() if count == 1]
	side_area = len(sides)
	
	enclosed_cubes = get_enclosed_cubes(cubes)
	enclosed_sides = list()
	for cube in enclosed_cubes:
		enclosed_sides += get_offset_cubes(cube, [-0.5, 0.5])

	enclosed_sides = [side for side, count in Counter(enclosed_sides).items() if count == 1]
	enclosed_sides_area = len(enclosed_sides)

	print(enclosed_cubes)
	print(side_area, enclosed_sides_area)
	print(side_area - enclosed_sides_area)

if __name__ == '__main__':
	# part_one()
	part_two()