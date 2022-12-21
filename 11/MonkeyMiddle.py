from functools import reduce
import re

def get_data(path):
	with open(path) as file:
		monkeys = file.read().split("\n\n")

	return monkeys

class Monkey:
	def __init__(self, monkey_string, monkeys):
		# Parse monkey_string
		rows = monkey_string.split("\n")
		self.number = int(re.findall(r"([0-9]+)", rows[0])[0])
		self.items = [int(item) for item in re.findall(r"Starting items: (.+)", rows[1])[0].split(",")]
		op_string = re.findall(r"Operation: new = (.+)", rows[2])[0]
		self.op = lambda old: eval(op_string)
		self.test_div = int(re.findall(r"[0-9]+", rows[3])[0]) 
		self.worry_div = 3
		self.worry_mod = 1
		self.throw_monkeys = {True: int(re.findall(r"[0-9]+", rows[4])[0]), 
		False: int(re.findall(r"[0-9]+", rows[5])[0])}

		self.monkeys = monkeys
		self.num_inspects = 0

	def __str__(self):
		string = f"Monkey {self.number}. Items: {self.items}\n" 
		# string += f"Op: {self.op}. Test div: {self.test_div}\n"
		# string += f"Throws: {self.throw_monkeys}\n"
		return string

	def one_round(self):
		while self.items:
			worry = self.items.pop(0)
			worry = self.op(worry)
			worry //= self.worry_div
			worry %= self.worry_mod

			test_ok = worry % self.test_div == 0 
			self.monkeys[self.throw_monkeys[test_ok]].items.append(worry)
			self.num_inspects += 1

def part_one():
	monkey_strings = get_data("input.txt")
	
	monkeys = dict()
	for string in monkey_strings:
		monkey = Monkey(string, monkeys)
		monkeys[monkey.number] = monkey

	num_rounds = 20
	for _ in range(num_rounds):
		for monkey in monkeys.values():
			monkey.one_round()

	inspects = sorted([monkey.num_inspects for monkey in monkeys.values()])
	print(inspects[-1] * inspects[-2])

def part_two():
	monkey_strings = get_data("input.txt")
	
	monkeys = dict()
	for string in monkey_strings:
		monkey = Monkey(string, monkeys)
		monkey.worry_div = 1
		monkeys[monkey.number] = monkey

	worry_mod = reduce(lambda x, y: x*y, [monkey.test_div for monkey in monkeys.values()])
	for monkey in monkeys.values():
		monkey.worry_mod = worry_mod

	num_rounds = 10000
	for _ in range(num_rounds):
		for monkey in monkeys.values():
			monkey.one_round()

	inspects = sorted([monkey.num_inspects for monkey in monkeys.values()])
	print(inspects[-1] * inspects[-2])


if __name__ == '__main__':
	part_one()
	part_two()