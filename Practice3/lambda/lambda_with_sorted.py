words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

"""Sorts words by their length (shortest to longest).
Output: ['pie', 'apple', 'banana', 'cherry']"""