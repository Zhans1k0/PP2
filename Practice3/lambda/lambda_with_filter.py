numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)

"""The code filters the list to keep only even numbers.

filter(lambda x: x % 2 == 0, numbers) checks each number in numbers.

x % 2 == 0 is True for even numbers (2, 4, 6, 8).

list() converts the result to a list.

Output: [2, 4, 6, 8]"""