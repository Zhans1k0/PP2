from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
names = ["  антон  ", "МАРИЯ", "иван"]


squares = list(map(lambda x: x ** 2, numbers))
print(f"Квадраты: {squares}")


clean_names = list(map(lambda n: n.strip().title(), names))
print(f"Очищенные имена: {clean_names}")


evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Чётные числа: {evens}")


total = reduce(lambda acc, x: acc + x, numbers)
print(f"Сумма всех чисел: {total}")

product = reduce(lambda acc, x: acc * x, numbers)
print(f"Произведение всех чисел: {product}")

even_squares = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
print(f"Квадраты чётных чисел: {even_squares}")