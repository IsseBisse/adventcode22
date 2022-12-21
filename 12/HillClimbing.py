import numpy as np
import sys

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	hill_map = np.zeros((len(data), len(data[0])))
	for row_idx, string in enumerate(data):
		for col_idx, char in enumerate(string):
			hill_map[row_idx, col_idx] = ord(char)
			if char == "S":
				start = (row_idx, col_idx)
				hill_map[row_idx, col_idx] = ord("a")
			elif char == "E":
				end = (row_idx, col_idx)
				hill_map[row_idx, col_idx] = ord("z")

	return hill_map, start, end

def get_connected_unvisited_nodes(pos, hill_map, visited):
	next_pos = list()
	dim = hill_map.shape
	for move in [(1,0), (0,1), (-1,0), (0, -1)]:
		new_pos = np.array(pos) + np.array(move)
		if all(new_pos >= (0, 0)) and all(new_pos < dim) and \
			hill_map[tuple(new_pos)]-1 <= hill_map[pos] and \
			tuple(new_pos) not in visited:
			next_pos.append(tuple(new_pos))

	return next_pos

def dijkstra(risk_matrix, start):
	cost_matrix = np.full(risk_matrix.shape, np.inf)
	cost_matrix[0, 0] = 0

	finish = tuple([dim-1 for dim in risk_matrix.shape])

	unvisited_non_infinite = [(0, start)]
	visited = set()

	while unvisited_non_infinite:
		# Hugely inefficient but works for now
		unvisited_non_infinite.sort(key=lambda x: x[0])

		currend_node = unvisited_non_infinite[0]
		current_score, current_pos = currend_node
		connected_nodes = get_connected_unvisited_nodes(current_pos, risk_matrix, visited)

		# print(currend_node, connected_nodes)

		for next_node in connected_nodes:
			x, y = next_node
			next_cost = current_score+1
			if next_cost < cost_matrix[x, y]:
				cost_matrix[x, y] = next_cost
				unvisited_non_infinite.append((next_cost, next_node))

		# print(cost_matrix)

		unvisited_non_infinite.remove(currend_node)
		visited.add(current_pos)

	return cost_matrix

def part_one():
	hill_map, start, end = get_data("input.txt")
	cost_map = dijkstra(hill_map, start)
	print(cost_map[end])

def part_two():
	hill_map, _, end = get_data("input.txt")
	possible_starts = np.where(hill_map==ord("a"))

	shortest_path = 1e9
	for start in zip(*possible_starts):
		cost_map = dijkstra(hill_map, start)
		path = cost_map[end]

		shortest_path = path if path < shortest_path else shortest_path

	print(shortest_path)

if __name__ == '__main__':
	part_one()
	part_two()