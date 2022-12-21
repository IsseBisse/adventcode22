def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [tuple([parts for parts in row.split(" ")]) for row in data]

	return data

OPP_TO_VALUE = {chr(65+i): i for i in range(3)}
YOU_TO_VALUE = {chr(88+i): i for i in range(3)}

def part_one():
	rounds = get_data("input.txt")

	your_score = 0
	for opp, you in rounds:
		opp_val = OPP_TO_VALUE[opp]
		you_val = YOU_TO_VALUE[you]

		your_score += you_val + 1
		if you_val - opp_val == 0:
			# Draw
			your_score += 3

		elif ((you_val - 1) % 3) == opp_val:
			# Win
			your_score += 6

	print(your_score)

def part_two():
	rounds = get_data("input.txt")

	your_score = 0
	for opp, outcome in rounds:
		opp_val = OPP_TO_VALUE[opp]
		outcome_val = YOU_TO_VALUE[outcome] 	# 0 = lose, 1 = draw, 2 = win

		if outcome_val == 0:
			# Lose
			you_val = (opp_val - 1) % 3
			your_score += you_val + 1

		elif outcome_val == 2:
			# Win
			you_val = (opp_val + 1) % 3
			your_score += you_val + 1 + 6

		else:
			# Draw
			you_val = opp_val
			your_score += you_val + 1 + 3

	print(your_score)

if __name__ == '__main__':
	part_one()
	part_two()
