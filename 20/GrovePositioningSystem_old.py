def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    data = [int(row) for row in data]

    return data


def move(numbers, number, steps):
    idx = numbers.index(number)
    steps = steps-1 if steps < 0 else steps
    steps = steps+1 if idx+steps > len(numbers) else steps

    new_idx = (idx + steps) % len(numbers)
    del numbers[idx]
    numbers.insert(new_idx, number)

    return numbers


def mix(numbers):
    indices = list(range(len(numbers)))

    for idx, steps in enumerate(numbers):
        indices = move(indices, idx, steps)
        print([numbers[idx2] for idx2 in indices])

    numbers = [numbers[idx] for idx in indices]
    return numbers


def part_one():
    numbers = get_data("smallInput.txt")
    numbers = [3, 1, 0]
    numbers = [0, -1, -1, 1]
    print(numbers)
    numbers = mix(numbers)
    print(numbers)

    groove_coord = 0
    for value in [1000, 2000, 3000]:
        idx = (numbers.index(0) + value) % len(numbers)
        # print(idx, numbers[idx])
        groove_coord += numbers[idx]

    print(groove_coord)

def part_two():
    data = get_data("smallInput.txt")


if __name__ == '__main__':
    part_one()
    part_two()
