"""Sample calculator module with intentional issues for demo reviews."""

import os
import sys


def calc(x, y, op):
    if op == "add":
        return x + y
    elif op == "sub":
        return x - y
    elif op == "mul":
        return x * y
    elif op == "div":
        return x / y  # No zero-division check
    else:
        return None


def process_numbers(numbers):
    total = 0
    unused_var = 42
    for i in range(len(numbers) + 1):  # Off-by-one bug
        total += numbers[i]
    return total


def read_config(path):
    f = open(path)
    data = f.read()
    return data  # File never closed; no exception handling


class dataProcessor:
    def __init__(self, items):
        self.items = items

    def filter_positive(self):
        result = []
        for item in self.items:
            if item > 0:
                result.append(item)
        return result

    def average(self):
        return sum(self.items) / len(self.items)  # Empty list crash


def main():
    a = 10
    b = 0
    print(calc(a, b, "div"))
    nums = [1, 2, 3]
    print(process_numbers(nums))
    dp = dataProcessor([])
    print(dp.average())


if __name__ == "__main__":
    main()
