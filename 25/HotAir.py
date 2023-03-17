import itertools


def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data


CHAR_TO_NUM = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
NUM_TO_CHAR = {value: key for key, value in CHAR_TO_NUM.items()}


def to_dec(snafu):
	dec = 0
	base = 1
	for char in reversed(snafu):
		dec += CHAR_TO_NUM[char] * base
		base *= 5

	return dec


def to_snafu(dec):
	if dec == 0:
		return [0]

	digits = list()
	while dec:
		digit = (dec + 2) % 5
		digits.append(NUM_TO_CHAR[digit-2])
		dec = (dec + 2) // 5

	return "".join(digits[::-1])

def part_one():
	snafu_numbers = get_data("input.txt")

	# snafu_numbers = list()
	# snafu_numbers += ["".join(perm) for perm in itertools.product(CHAR_TO_NUM.keys(), repeat=3)]

	# dec_snafu = [(snafu, to_dec(snafu)) for snafu in snafu_numbers]
	# dec_snafu = sorted(dec_snafu, key=lambda item: item[1])
	# for snafu, dec in dec_snafu:
	# 	print(dec, snafu, to_snafu(dec))

	dec_sum = sum(to_dec(snafu) for snafu in snafu_numbers)
	print(dec_sum, to_snafu(dec_sum))

def part_two():
	data = get_data("smallInput.txt")

if __name__ == '__main__':
	part_one()
	part_two()