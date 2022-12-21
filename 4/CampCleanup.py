import numpy as np

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [tuple([tuple([int(num) for num in range_.split("-")]) for range_ in row.split(",")]) for row in data]

	return data

def contains(row):
	starts = [start for start, end in row]
	ends = [end for start, end in row]
	first_idx = set([idx for idx, value in enumerate(starts) if value == min(starts)])
	last_idx = set([idx for idx, value in enumerate(ends) if value == max(ends)])

	return len(first_idx.intersection(last_idx)) >= 1

def part_one():
	data = get_data("input.txt")
	
	contained_rows = list(filter(contains, data))
	print(len(contained_rows))

def overlaps(row):
	(first_start, first_end), (second_start, second_end) = row
	return (first_end >= second_start and first_start <= second_end) or \
		(second_end >= first_start and second_start <= first_end)

def part_two():
	data = get_data("input.txt")
	overlapping_rows = list(filter(overlaps, data))
	print(len(overlapping_rows))

if __name__ == '__main__':
	part_one()
	part_two()
