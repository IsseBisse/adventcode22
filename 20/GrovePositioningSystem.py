from dataclasses import dataclass
from typing import TypeVar


def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    data = [int(row) for row in data]

    return data


Node = TypeVar("Node")
@dataclass
class Node:
    value: int
    is_head: bool = False
    next_: Node = None
    prev: Node = None

    def __str__(self):
        return f"...{self.prev.value}, {self.value}, {self.next_.value}..."


    @staticmethod
    def swap(left, right):
        old_prev = left.prev
        old_next = right.next_
        left.prev = right
        left.next_ = old_next
        right.prev = old_prev
        right.next_ = left
        old_prev.next_ = right
        old_next.prev = left

        # temp = left.is_head
        # left.is_head = right.is_head
        # right.is_head = temp

    def swap_left(self):
        Node.swap(self.prev, self)


    def swap_right(self):
        Node.swap(self, self.next_)


class CircularList:
    def __init__(self, list_):
        self.original_order_list = [Node(value) for value in list_]
        for idx, node in enumerate(self.original_order_list):
            node.next_ = self.original_order_list[(idx+1)%len(self.original_order_list)]
            node.prev = self.original_order_list[idx-1]
        self.original_order_list[0].is_head = True
        

    def __str__(self):
        head = self.original_order_list[0]
        current = head
        string = f"[{current.value}"
        current = current.next_
        while current != head:
            string += f", {current.value}"
            current = current.next_
        
        string += "]"
        return string

    def mix(self):
        div = len(self.original_order_list) - 1
        
        for node in self.original_order_list:
            if node.value == 0:
                continue

            num_laps = abs(node.value) % div
            # num_laps = abs(node.value)
            if node.value < 0:
                for _ in range(num_laps):
                    node.swap_left()

            else:
                for _ in range(num_laps):
                    node.swap_right()
       
        # for node in self.original_order_list:

    def coordinates(self):
        current = self.original_order_list[0]
        while current.value != 0:
            current = current.next_

        coords = list()
        for _ in range(3):
            for _ in range(1000):
                current = current.next_

            coords.append(current.value)

        return coords


def part_one():
    data = get_data("input.txt")
    circular_list = CircularList(data)
    # print(circular_list)
    circular_list.mix()
    # print(circular_list)
    coords = circular_list.coordinates()
    print(sum(coords))


def part_two():
    data = get_data("input.txt")
    decryption_key = 811589153
    data = [decryption_key*value for value in data]
    circular_list = CircularList(data)
    for _ in range(10):
        circular_list.mix()
    coords = circular_list.coordinates()
    print(sum(coords))


if __name__ == '__main__':
    # part_one()
    part_two()