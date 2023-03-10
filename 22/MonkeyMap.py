import math
import matplotlib.pyplot as plt
import numpy as np
import re


def string_to_board(string):
	walls = dict()
	for y, row in enumerate(string.split("\n")):
		walls[y] = dict()
		for x, char in enumerate(row):
			if char == "#":
				walls[y][x] = True

			elif char == ".":
				walls[y][x] = False

	return walls


def get_data(path):
	with open(path) as file:
		board, path = file.read().split("\n\n")

	path = re.findall(r"[0-9]+|[R|L]", path)
	path = [int(string) if string.isdigit() else string for string in path]

	board = string_to_board(board)

	return board, path


def get_starting_position(board):
	y = 0
	x = min(board[y].keys())
	return np.array([x, y])


def is_outside(coords, board):
	x, y = coords
	return y not in board or x not in board[y]


def is_wall(coords, board):
	x, y = coords
	return board[y][x]


def wrap_around_row(direction, row):
	if direction > 0:
		return min(row)

	else:
		return max(row)


def wrap_around(coords, direction, board):
	x, y = coords
	x_dir, y_dir = direction
	if y_dir == 0:
		# Horizontal
		row = board[y].keys()
		x = wrap_around_row(x_dir, row)
		
	else:
		# Vertical
		row = [y for y in board.keys() if x in board[y]]
		y = wrap_around_row(y_dir, row)

	next_coords = np.array([x, y])
	return next_coords


def next_position(coords, direction, board):
	next_coords = coords + direction
	if is_outside(next_coords, board):
		next_coords = wrap_around(coords, direction, board)


	next_coord_is_wall = is_wall(next_coords, board)
	if is_wall(next_coords, board):
		return coords

	else:
		return next_coords

class Mover:
	ROTATION = {"L": np.array([[0, -1], [1, 0]]),
				"R": np.array([[0, 1], [-1, 0]])}
	DIRECTION_TO_INT = {(1, 0): 0,
						(0, 1): 1,
						(-1, 0): 2,
						(0, -1): 3}

	def __init__(self, board, path):
		self.board = board
		self.position = get_starting_position(board)
		self.direction = np.array([1, 0])
		self.path = path

	def __str__(self):
		return f"{self.position} facing {self.direction}"

	def one_step(self, instruction):
		if isinstance(instruction, str):
			self.direction = np.matmul(self.direction, self.ROTATION[instruction])

		else:
			for _ in range(instruction):
				self.position = next_position(self.position, self.direction, self.board)

	def move(self):
		for instruction in self.path:
			# print(instruction)
			self.one_step(instruction)
			# print(self)

	def password(self):
		col, row = self.position + np.array([1, 1])
		facing = self.DIRECTION_TO_INT[tuple(self.direction)]

		password = 1000*row + 4*col + facing
		return password

def part_one():
	board, path = get_data("input.txt")
	mover = Mover(board, path)

	mover.move()
	print(mover.password())


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


class Voxel:
	def __init__(self, coords, is_wall=False):
		self.coords_2d = coords[:2]
		self.coords = np.array(coords)
		self.is_wall = is_wall
		self.normal = np.array((0, 0, -1))
		# TODO: Add connected voxels

	def __str__(self):
		return f"{tuple(self.coords)} normal {tuple(self.normal)}"

	def transform(self, transformation_vector):
		transformation_vector = np.array(transformation_vector)
		self.coords = self.coords + transformation_vector

	def rotate_and_transform(self, transformation_vector, axis, theta):
		self.transform(tuple([-t for t in transformation_vector]))
		coords = np.dot(rotation_matrix(axis, theta), self.coords)
		normal = np.dot(rotation_matrix(axis, theta), self.normal)
		self.coords = np.round(coords, decimals=1)
		self.normal = np.round(normal, decimals=1)
		self.transform(transformation_vector)


def plot(voxels):
	dots = [[voxel.coords[axis] for voxel in voxels if not voxel.is_wall] for axis in range(3)]
	walls = [[voxel.coords[axis] for voxel in voxels if voxel.is_wall] for axis in range(3)]
	normals = [[voxel.coords[axis]+voxel.normal[axis] for voxel in voxels] for axis in range(3)]	

	fig = plt.figure()
	ax = fig.add_subplot(projection="3d")
	ax.scatter(*dots, c="green", marker="o")
	ax.scatter(*walls, c="red", marker="o")
	# ax.scatter(*normals, marker="x")

	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")


class VoxelMover:
	ROTATION_TO_ANGLE = {"R": -np.pi/2,
						 "L": np.pi/2}
	DIRECTION_TO_INT = {(1, 0): 0,
						(0, 1): 1,
						(-1, 0): 2,
						(0, -1): 3}

	def __init__(self, voxel):
		self.voxel = voxel
		self.direction = np.array((1, 0, 0))
		self.normal = np.array((0, 0, -1))
		
	def add_voxels(self, voxels_dict):
		self.voxels_dict = voxels_dict

	def __str__(self):
		return f"On {str(self.voxel)} facing {tuple(self.direction)}"
	
	def rotate(self):
		new_normal = self.voxel.normal
		axis = np.cross(self.normal, new_normal)
		theta = np.arccos(np.dot(self.normal, new_normal))
		direction = np.dot(rotation_matrix(axis, theta), self.direction)

		self.direction = np.round(direction, decimals=1)
		self.normal = np.round(new_normal, decimals=1)

	def move(self, path):
		for instruction in path:
			self.one_turn(instruction)

	def one_turn(self, instruction):
		if isinstance(instruction, str):
			theta = self.ROTATION_TO_ANGLE[instruction]
			self.direction = np.round(np.dot(rotation_matrix(self.normal, theta), self.direction), decimals=1)

		else:
			for _ in range(instruction):
				self.one_step()
				print(self.voxel.coords)
				print(self.voxel.coords_2d)

	def one_step(self):
		coords = self.voxel.coords
		new_coords = np.round(coords + self.direction, decimals=1)
		new_coords_key = tuple(new_coords)
		change_side = False
		if not new_coords_key in self.voxels_dict:
			new_coords = np.round(coords + 0.5*self.direction - 0.5*self.normal, decimals=1)
			new_coords_key = tuple(new_coords)
			change_side = True

		if not self.voxels_dict[new_coords_key].is_wall:
			self.voxel = self.voxels_dict[new_coords_key]

			if change_side:
				self.rotate()

	def password(self):
		col, row = tuple(self.voxel.coords_2d + np.array([1, 1]))
		facing = self.DIRECTION_TO_INT[tuple(self.direction[:2])]
		return 1000*row + 4*col + facing

small_input_rotations = [(lambda item: item[1] < 4, (0, 3.5, 0), (1, 0, 0), -np.pi/2),
			 			 (lambda item: item[0] >= 12, (11.5, 0, 0), (0, 1, 0), -np.pi/2),
			 			 (lambda item: item[0] < 4, (3.5, 0, 0), (0, 1, 0), np.pi/2),
			 			 (lambda item: item[0] < 8, (7.5, 0, 0), (0, 1, 0), np.pi/2),
			 			 (lambda item: item[1] >= 8, (0, 7.5, 0), (1, 0, 0), np.pi/2)]

input_rotations = [(lambda item: item[0] >= 100, (99.5, 0, 0), (0, 1, 0), -np.pi/2),
			 	   (lambda item: item[1] >= 150, (0, 149.5, 0), (1, 0, 0), np.pi/2),
			 	   (lambda item: item[1] < 50, (0, 49.5, 0), (1, 0, 0), -np.pi/2),
			 	   (lambda item: item[1] >= 100, (0, 99.5, 0), (1, 0, 0), np.pi/2),
			 	   (lambda item: item[0] < 50, (49.5, 99.5, 0), (0, 0, 1), np.pi/2)]


def part_two():
	# board, path = get_data("smallInput.txt")
	# rotations = small_input_rotations
	board, path = get_data("input.txt")
	rotations = input_rotations
	voxels = set()

	start_x, start_y = get_starting_position(board)
	for y in board:
		for x in board[y]:
			is_wall = board[y][x]
			voxel = Voxel((x, y, 0), is_wall)
			if x == start_x and y == start_y:
				mover = VoxelMover(voxel)
			voxels.add(voxel)
	
	
	for split_func, transform, axis, theta in rotations:
		side = {voxel for voxel in voxels if split_func(voxel.coords)}
		for voxel in side:
			voxel.rotate_and_transform(transform, axis, theta)

	# side = {voxel for voxel in voxels if voxel.coords[0]<50}
	# for voxel in side:
	# 	voxel.transform((-49.5, -99.5, 0))

	# plot(voxels)

	# for voxel in side:	
	# 	voxel.rotate_and_transform((0, 0, 0), (0, 0, 1), np.pi/2)
	# 	# voxel.rotate_and_transform(transform, axis, theta)

	mover.rotate()

	for voxel in voxels:
		voxel.transform((-7.5, -3.5, 0))

	voxels_dict = {tuple(voxel.coords): voxel for voxel in voxels}
	mover.add_voxels(voxels_dict)
	
	plot(voxels)
	plt.show()

	mover.move(path)
	print(mover.password())

if __name__ == '__main__':
	# part_one()
	part_two()