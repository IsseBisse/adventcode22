import numpy as np

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [[int(char) for char in row] for row in data]
	data = np.array(data)

	return data

def visible_along_line(line):
	line_max = -1
	visible = list()
	for idx, value in enumerate(line):
		if value > line_max:
			visible.append(idx)
			line_max = value

	return visible

def visible_from_side(tree_map):
	visible = list()
	height, width = tree_map.shape
	for row_idx in range(height):
		row = tree_map[row_idx, :]
		visible += [(row_idx, col_idx) for col_idx in visible_along_line(row)]
		visible += [(row_idx, width-col_idx-1) for col_idx in visible_along_line(row[::-1])]

	for col_idx in range(width):
		col = tree_map[:, col_idx]
		visible += [(row_idx, col_idx) for row_idx in visible_along_line(col)]
		visible += [(height-row_idx-1, col_idx) for row_idx in visible_along_line(col[::-1])]

	return set(visible)


def part_one():
	tree_map = get_data("input.txt")
	visible_trees = visible_from_side(tree_map)
	print(len(visible_trees))
	
	# visible_map = np.zeros_like(tree_map)
	# for row_idx, col_idx in visible_trees:
	# 	visible_map[row_idx, col_idx] = 1

	# print(visible_map)

def viewing_distance(line, height):
	idx = 0
	while idx < len(line) and line[idx] < height:
		idx += 1

	if idx == len(line):
		idx -= 1
	idx += 1

	return idx

def viewing_distance_map(tree_map):
	viewing_distance_map = np.zeros_like(tree_map)
	# viewing_distance_map = np.zeros((*tree_map.shape, 4))

	height, width = tree_map.shape
	for row_idx in range(height):
		for col_idx in range(width):
			distance = 1
			distance = viewing_distance(tree_map[row_idx, col_idx+1:], tree_map[row_idx, col_idx])
			distance *= viewing_distance(tree_map[row_idx, :col_idx][::-1], tree_map[row_idx, col_idx])
			distance *= viewing_distance(tree_map[row_idx+1:, col_idx], tree_map[row_idx, col_idx])
			distance *= viewing_distance(tree_map[:row_idx, col_idx][::-1], tree_map[row_idx, col_idx])
			viewing_distance_map[row_idx, col_idx] = distance

	return viewing_distance_map

def part_two():
	tree_map = get_data("input.txt")
	distance_map = viewing_distance_map(tree_map)

	# print(tree_map)
	# print(distance_map)
	print(np.max(distance_map))

if __name__ == '__main__':
	part_one()
	part_two()