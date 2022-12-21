from operator import add, sub, mul, truediv, eq
from decimal import *

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [row.split(": ") for row in data]
	data = [(row[0], row[1].split(" ")) for row in data]

	return data

def parse_func_list(monkeys, func_list):
	OP_TO_FUNC = {"+": add,
				  "-": sub,
				  "*": mul,
				  "/": truediv,
				  "=": eq}

	if len(func_list) == 1:
		value = Decimal(func_list[0])
		return lambda: value

	else:
		a_key, op, b_key = func_list
		func = OP_TO_FUNC[op]
		return lambda: func(monkeys[a_key], monkeys[b_key])

class Monkey:
	def __init__(self):
		self.value = None

	def __add__(self, other):
		return self.value() + other.value()

	def __sub__(self, other):
		return self.value() - other.value()

	def __mul__(self, other):
		return self.value() * other.value()

	def __truediv__(self, other):
		return self.value() / other.value()

	def __eq__(self, other):
		return self.value() == other.value()

def part_one():
	data = get_data("input.txt")

	monkeys = dict()
	for name, _ in data:
		monkeys[name] = Monkey()
	for name, func_list in data:
		monkeys[name].value = parse_func_list(monkeys, func_list)

	print(monkeys["root"].value())

def part_two():
	data = get_data("input.txt")
	row_idx = [idx for idx, (name, _) in enumerate(data) if name == "root"][0]
	data[row_idx][1][1] = "="

	monkeys = dict()
	for name, _ in data:
		monkeys[name] = Monkey()
	for name, func_list in data:
		monkeys[name].value = parse_func_list(monkeys, func_list)

	a_key, b_key = data[row_idx][1][0], data[row_idx][1][-1]
	a = list()
	b = list()
	x = range(0, 1000000, 1000)
	for value in [0, 1]:
		monkeys["humn"].value = lambda: value

		a.append(monkeys[a_key].value())
		b.append(monkeys[b_key].value())

	print(a, b)

	y = b[0]
	k = a[1] - a[0]
	m = a[0]

	x = (y-m)/k
	print(x)

	value = int(x)
	monkeys["humn"].value = lambda: value
	incr = 1 if monkeys[a_key].value() > monkeys[b_key].value() else -1

	while not monkeys["root"].value():
		value += incr

	print(value)

if __name__ == '__main__':
	#part_one()
	part_two()