from collections import defaultdict
from dataclasses import dataclass, field
from functools import partial
from multiprocessing import Pool
import re
from typing import Dict
from tqdm import tqdm

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	blueprints = [get_blueprint(row) for row in data]

	return blueprints

def get_cost(sentence):
	material_cost = {material: 0 for material in MATERIALS}
	output = re.findall(r"([a-z]+) robot", sentence)[0]
	materials = re.findall(r"[0-9]+ [a-z]+", sentence)

	for cost_string in materials:
		value = int(cost_string.split(" ")[0])
		material = cost_string.split(" ")[1]

		material_cost[material] = value

	return output, material_cost

def get_blueprint(row):
	sentences = row.split(":")[1].split(".")[:-1]
	robot_costs = [get_cost(sentence) for sentence in sentences]
	robot_costs = {robot: cost for robot, cost in robot_costs}

	return robot_costs

MATERIALS = ("ore", "clay", "obsidian", "geode")

@dataclass
class State:
	materials: Dict[str, int] = field(default_factory = lambda: ({material: 0 for material in MATERIALS}))
	robots: Dict[str, int] = field(default_factory = lambda: ({robot: 0 for robot in MATERIALS}))

	def one_turn(self):
		for material in self.materials:
			self.materials[material] += self.robots[material]
		
	def copy(self):
		return State({material: amount for material, amount in self.materials.items()}, {robot: amount for robot, amount in self.robots.items()})

	def build(self, robot, cost):
		for material in self.materials:
			self.materials[material] -= cost[material]
		self.robots[robot] += 1

	def __le__(self, other):
		for self_robot, other_robot in zip(self.robots.values(), other.robots.values()):
			if self_robot > other_robot:
				return False

		for self_material, other_material in zip(self.materials.values(), other.materials.values()):
			if self_material > other_material:
				return False

		return True

def one_turn(state, robot_costs):
	next_state = state.copy()
	next_state.one_turn()
		
	max_robot_amount = {material: max([robot_cost[material] for robot_cost in robot_costs.values()]) for material in MATERIALS}
	max_robot_amount["geode"] = 25

	possible_next_states = list()
	for robot, cost in robot_costs.items():
		if not all([available >= required for available, required in zip(state.materials.values(), cost.values())]):
			# Can't afford it
			continue

		if state.robots[robot] >= max_robot_amount[robot]:
			# No more robots of that type needed
			continue

		new_robot_state = next_state.copy()
		new_robot_state.build(robot, cost)
		possible_next_states.append(new_robot_state)

	possible_next_states.append(next_state)
	return possible_next_states

def exists_strictly_better_state(state, idx, all_states):
	for other_idx, other_state in enumerate(all_states):
		if idx == other_idx:
			continue

		if state <= other_state:
			return True

	return False

def test_blueprint(blueprint, num_turns=24):
	start_state = State()
	start_state.robots["ore"] = 1

	states = [start_state]
	for turn in range(num_turns):
		next_states = list()
		for state in states:
			next_states += one_turn(state, blueprint)

		# Remove strictly worse states
		same_robot_states = defaultdict(lambda: list())
		for state in next_states:
			robot_string = "-".join(str(value) for value in state.robots.values())
			same_robot_states[robot_string].append(state)

		# Only compare against states with same amount of robots
		# Thoretically slightly less strict, but MUCH faster
		best_states = list()
		for same_robot_state in same_robot_states.values():
			best_same_robot_states = list()
			for idx, state in enumerate(same_robot_state):
				if not exists_strictly_better_state(state, idx, same_robot_state):
					best_same_robot_states.append(state) 

			best_states += best_same_robot_states

		states = best_states
		
	states = sorted(states, key=lambda item: item.materials["geode"])
	print("Done!")
	return states[-1]

def part_one():
	blueprints = get_data("input.txt")
	
	quality_level = list()
	for idx, blueprint in enumerate(tqdm(blueprints)):
		best_state = test_blueprint(blueprint)
		quality_level.append((idx+1) * best_state.materials["geode"])

	print(sum(quality_level))


def part_two():
	blueprints = get_data("input.txt")
	
	blueprint_tester = partial(test_blueprint, num_turns=32)
	with Pool() as pool:
		best_states = pool.map(blueprint_tester, blueprints)

	non_index_adjusted_quality_level = [state.materials["geode"] for state in best_states]
	quality_level = [(idx+1)*level for idx, level in enumerate(non_index_adjusted_quality_level)]
	print(sum(quality_level))

if __name__ == '__main__':
	# part_one()
	part_two()

