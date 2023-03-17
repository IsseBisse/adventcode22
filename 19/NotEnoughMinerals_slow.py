from math import ceil
import re


def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	blueprints = [(idx+1, get_blueprint(row)) for idx, row in enumerate(data)]

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
	blueprints = [get_cost(sentence) for sentence in sentences]
	blueprints = {robot: cost for robot, cost in blueprints}

	return blueprints

MATERIALS = ("ore", "clay", "obsidian", "geode")


def time_to_buy(inventory, robots, recipe):
	additional_inventory = dict()
	minutes_to_buy = list()

	non_zero_recipe = {key: value for key, value in recipe.items() if value > 0}
	for material in non_zero_recipe:
		additional_inventory = recipe[material] - inventory[material]
		
		if robots[material] == 0:
			return None


		minutes_to_buy.append(max(0, ceil(additional_inventory / robots[material])))

	if len(minutes_to_buy) == 0:
		return None

	# Add one minute for build time
	minutes_to_buy = max(minutes_to_buy) + 1
	return minutes_to_buy


def fastforward(inventory, robots, minutes, recipe=None):
	new_inventory = dict()
	for material in inventory:
		new_inventory[material] = inventory[material] + minutes * robots[material]
		new_inventory[material] -= recipe[material] if recipe is not None else 0

	return new_inventory


def add_robot(robots, material):
	new_robots = {key: value for key, value in robots.items()}
	new_robots[material] += 1
	return new_robots


def theoretical_max_geodes(inventory, robots, minutes_left):
	max_geodes = inventory["geode"] + sum(range(robots["geode"], robots["geode"]+minutes_left))
	return max_geodes


def blueprint_tester(blueprint):
	max_robot_amount = {material: max(cost[material] for cost in blueprint.values()) for material in MATERIALS}
	max_robot_amount["geode"] = -1
	
	def best_path(state, minutes_left):
		inventory, robots = state
		
		path_geodes = list()
		for material in MATERIALS:
			if robots[material] == max_robot_amount[material]:
				continue

			recipe = blueprint[material]
			minutes_to_buy = time_to_buy(inventory, robots, recipe)
			if minutes_to_buy is None or minutes_to_buy > minutes_left:
				continue

			# print(state, minutes_left, material, minutes_to_buy)

			new_inventory = fastforward(inventory, robots, minutes_to_buy, recipe)
			new_robots = add_robot(robots, material)
			new_state = (new_inventory, new_robots)
			new_minutes_left = minutes_left - minutes_to_buy

			if len(path_geodes) == 0 or theoretical_max_geodes(new_inventory, new_robots, new_minutes_left) > max(path_geodes):
				geodes = best_path(new_state, new_minutes_left)
				path_geodes.append(geodes)

		if len(path_geodes) == 0:
			# No possible robot purchases. Run until end
			inventory = fastforward(inventory, robots, minutes_left)
			return inventory["geode"]
		
		else:
			return max(path_geodes)

	return best_path


def part_one():
	blueprints = get_data("input.txt")
	
	quality_level = list()
	for idx, blueprint in blueprints:
		best_path = blueprint_tester(blueprint)
		inventory = {material: 0 for material in MATERIALS}
		robots = {material: 0 for material in MATERIALS}
		robots["ore"] = 1
		state = (inventory, robots)
		minutes_left = 24

		geodes = best_path(state, minutes_left)
		quality_level.append(idx * geodes)
		print(f"Blueprint {idx} done!")
		
	print(quality_level)
	print(sum(quality_level))


def part_two():
	# blueprints = get_data("smallInput.txt")
	blueprints = get_data("input.txt")[:3]

	num_geodes = list()
	for idx, blueprint in blueprints:
		best_path = blueprint_tester(blueprint)
		inventory = {material: 0 for material in MATERIALS}
		robots = {material: 0 for material in MATERIALS}
		robots["ore"] = 1
		state = (inventory, robots)
		minutes_left = 28

		geodes = best_path(state, minutes_left)
		num_geodes.append(geodes)
		print(f"Blueprint {idx} done!")
		
	print(num_geodes)


if __name__ == '__main__':
	# part_one()
	part_two()
