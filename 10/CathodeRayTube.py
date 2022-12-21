import numpy as np

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [(row.split(" ")[0], None) if row.split(" ")[0] == "noop" else (row.split(" ")[0], int(row.split(" ")[1])) for row in data]

	return data

class CPU:
	def __init__(self):
		self.x = 1
		self.cycle_counter = -1

		self.signal_strength = list()
		self.screen = np.zeros((6, 40))

	def add_cycles(self, num_cycles=1):
		for _ in range(num_cycles):
			self.cycle_counter += 1
			if (self.cycle_counter+20) % 40 == 0:
				self.signal_strength.append(self.x * self.cycle_counter)

			self.update_screen()
			self.pretty_print()
			print("")

	def update_screen(self):
		row = self.cycle_counter // 40
		col = self.cycle_counter % 40

		if self.x-1 <= col <= self.x+1:
			self.screen[row, col] = 1

	def pretty_print(self):
		for row in range(self.screen.shape[0]):
			string = "".join(["#" if self.screen[row, col] == 1 else "." for col in range(self.screen.shape[1])])
			print(string)

	def run(self, command, arg):
		if command == "noop":
			self.add_cycles()

		elif command == "addx":
			self.add_cycles(2)
			self.x += arg

def part_one():
	commands = get_data("input.txt")
	cpu = CPU()
	
	for command, arg in commands:
		cpu.run(command, arg)

	print(sum(cpu.signal_strength))

def part_two():
	commands = get_data("input.txt")
	cpu = CPU()

	for command, arg in commands:
		cpu.run(command, arg)

	cpu.pretty_print()

if __name__ == '__main__':
	part_one()
	part_two()