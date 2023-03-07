from collections import defaultdict
from itertools import permutations
import re

def parse(string):
	valves = re.findall(r"[A-Z]{2}", string)
	name = valves[0]
	flow_rate = int(re.findall(r"rate=([0-9]+)", string)[0])
	connection_names = valves[1:]

	return name, flow_rate, connection_names

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = map(parse, data)

	return tuple(data)

class Node:
	def __init__(self, name, flow_rate):
		self.name = name
		self.flow_rate = flow_rate

	def __str__(self):
		return f"Node {self.name}, flow rate={self.flow_rate}, connected to: {[node.name for node in self.connections]}"

	def __repr__(self):
		return f"Node {self.name}"

	def add_connections(self, connections):
		self.connections = connections


def step(node, opened_valves, pressure, minutes_left):
	states = list()
	if node.flow_rate > 0 and node.name not in opened_valves: 
		# Open valve
		new_opened_valves = {valve for valve in opened_valves}
		new_opened_valves.add(node.name)
		states.append((node, new_opened_valves, pressure+node.flow_rate*(minutes_left-1)))

	for next_node in node.connections:
		new_opened_valves = {valve for valve in opened_valves}
		states.append((next_node, new_opened_valves, pressure))

	return states

def state_hash(current_node, opened_valves):
	return f"{current_node.name}_{'-'.join(sorted(opened_valves))}"

def part_one():
	data = get_data("input.txt")
	
	nodes = dict()
	for name, flow_rate, _ in data:
		nodes[name] = Node(name, flow_rate)
	for name, _, connections in data:
		nodes[name].add_connections([nodes[conn] for conn in connections]) 

	minutes_left = 30
	states = step(nodes["AA"], {}, 0, minutes_left)
	minutes_left -= 1
	best_states = {node: defaultdict(int) for node in nodes}
	while minutes_left > 0:
		for state in states:
			new_states = step(*state, minutes_left)
			
			for node, opened_valves, pressure in new_states:
				sorted_valve_string = "-".join(sorted(opened_valves))
				best_states[node.name][sorted_valve_string] = max(best_states[node.name][sorted_valve_string], pressure)

		states = list()
		for node_name, strings in best_states.items():
			for sorted_valve_string, pressure in strings.items():
				opened_valves = set(sorted_valve_string.split("-"))
				states.append((nodes[node_name], opened_valves, pressure))

		minutes_left -= 1
		print(minutes_left)

	states = sorted(states, key=lambda item: item[2])
	print(states[-1])

# VEEERY slow
def part_two():
	data = get_data("input.txt")

	nodes = dict()
	for name, flow_rate, _ in data:
		nodes[name] = Node(name, flow_rate)
	for name, _, connections in data:
		nodes[name].add_connections([nodes[conn] for conn in connections]) 

	node_pairs = set([f"{first}_{second}" for first, second in permutations(list(nodes.keys())+list(nodes.keys()), 2)])
	best_states = {node_pair: defaultdict(int) for node_pair in node_pairs}
	
	first = nodes["AA"] 
	second = nodes["AA"]
	opened_valves = {}
	pressure = 0
	states = [((first, second), opened_valves, pressure)]
	minutes_left = 26
	
	# next_states = list()
	# half_states = step(first, opened_valves, pressure, minutes_left)
	# for new_first, opened_valves, pressure in half_states:
	# 	other_half_states = step(second, opened_valves, pressure, minutes_left)
		
	# 	# Merge half-state
	# 	for new_second, opened_valves, pressure in other_half_states:
	# 		next_states.append(((new_first, new_second), opened_valves, pressure))
	# minutes_left -= 1
	while minutes_left > 0:
		for (first, second), opened_valves, pressure in states:
			half_states = step(first, opened_valves, pressure, minutes_left)
			
			new_states = list()
			for new_first, new_opened_valves, new_pressure in half_states:
				other_half_states = step(second, new_opened_valves, new_pressure, minutes_left)
		
				# Merge half-state
				for new_second, opened_valves, pressure in other_half_states:
					new_states.append(((new_first, new_second), opened_valves, pressure))

			# Only save best states
			for (new_first, new_second), opened_valves, pressure in new_states:
				node_pair = f"{new_first.name}_{new_second.name}"
				sorted_valve_string = "-".join(sorted(opened_valves))
				best_states[node_pair][sorted_valve_string] = max(best_states[node_pair][sorted_valve_string], pressure)

		# Create new states from best states
		states = list()
		for node_pair_name, strings in best_states.items():
			for sorted_valve_string, pressure in strings.items():
				opened_valves = set(sorted_valve_string.split("-"))
				first_node_name, second_node_name = node_pair_name.split("_")
				states.append(((nodes[first_node_name], nodes[second_node_name]), opened_valves, pressure))

		minutes_left -= 1
		print(minutes_left)


	states = sorted(states, key=lambda item: item[2])
	print(states[-1])

if __name__ == '__main__':
	# part_one()
	part_two()