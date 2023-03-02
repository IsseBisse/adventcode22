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

def part_one():
	data = get_data("smallInput.txt")
	print(data)
	
def part_two():
	data = get_data("smallInput.txt")

if __name__ == '__main__':
	part_one()
	part_two()