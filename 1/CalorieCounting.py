def get_data(path):
	with open(path) as file:
		data = file.read().split("\n\n")

	data = [[int(cal) for cal in row.split("\n")] for row in data]
	
	return data

def part_one():
	calories = get_data("input.txt")
	total_calories = [sum(cal) for cal in calories]
	print(max(total_calories))

def part_two():
	calories = get_data("input.txt")
	total_calories = [sum(cal) for cal in calories]
	total_calories.sort(reverse=True)
	print(sum(total_calories[:3]))

if __name__ == '__main__':
	part_one()
	part_two()