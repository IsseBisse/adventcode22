from dataclasses import dataclass
from typing import TypeVar

def get_data(path):
	with open(path) as file:
		data = file.read().split("$ ")

	commands = [row.split("\n") for row in data][1:]
	commands = [(item[0], [arg for arg in item[1:] if arg != ""]) if item[0] == "ls" else (item[0][:2], item[0][3:]) for item in commands]

	return commands

@dataclass
class File:
	name: str
	size: int

	def print(self, indent=0):
		string = " " * indent
		string += f"- {self.name} (file, size={self.size})"
		print(string)

	def get_size(self):
		return self.size

Directory = TypeVar("Directory")
@dataclass
class Directory:
	name: str
	parent: Directory
	children: dict = None

	def print(self, indent=0):
		string = " " * indent
		string += f"- {self.name} (dir)"
		print(string)
		for _, child in self.children.items():
			child.print(indent+2)

	def add_child(self, key, child):
		if self.children is None:
			self.children = {key: child}

		else:
			self.children[key] = child

	def get_child(self, key):
		return self.children[key]

	def get_parent(self):
		return self.parent

	def get_size(self):
		size = 0
		for _, child in self.children.items():
			size += child.get_size()

		return size

	def get_all_subsizes(self):
		sizes = [(self.name, self.get_size())]
		for _, child in self.children.items():
			if isinstance(child, Directory):
				sizes += child.get_all_subsizes()

		return sizes

@dataclass
class FileSystem:
	root: Directory
	ptr: Directory = None

	def cd(self, arg):
		if arg == "/":
			self.ptr = self.root

		elif arg == "..":
			self.ptr = self.ptr.get_parent()

		else:
			self.ptr = self.ptr.get_child(arg)

	def ls(self, args):
		for arg in args:
			first, key = arg.split(" ")
			if first == "dir":
				self.ptr.add_child(key, Directory(key, self.ptr))

			else:
				self.ptr.add_child(key, File(key, int(first)))

	def execute_command(self, command, args):
		if command == "cd":
			self.cd(args)
		elif command == "ls":
			self.ls(args)

def part_one():
	data = get_data("input.txt")
	root = Directory("/", None)
	filesystem = FileSystem(root)

	for command, args in data:
		filesystem.execute_command(command, args)

	# filesystem.root.print()
	# print(filesystem.root.get_size())
	directory_sizes = [item for item in filesystem.root.get_all_subsizes() if item[1] < 100000]
	# print(directory_sizes)
	print(sum([size for name, size in directory_sizes]))
	
def part_two():
	data = get_data("input.txt")
	root = Directory("/", None)
	filesystem = FileSystem(root)

	for command, args in data:
		filesystem.execute_command(command, args)

	total_space = 70000000
	unused_space = total_space - filesystem.root.get_size()
	required_space = 30000000

	directory_sizes = [item for item in filesystem.root.get_all_subsizes() if item[1]+unused_space > required_space]
	directory_sizes = sorted(directory_sizes, key=lambda item: item[1])
	print(directory_sizes[0])

if __name__ == '__main__':
	part_one()
	part_two()