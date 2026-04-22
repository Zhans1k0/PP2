my_list = [1, 2, 3, 4]

my_iter = iter(my_list)

print(next(my_iter))
print(next(my_iter))

for x in my_iter:
    print(x)


class CountUp:
    def init(self, max_value):
        self.max = max_value
        self.current = 0

    def iter(self):
        return self

    def next(self):
        if self.current < self.max:
            self.current += 1
            return self.current
        else:
            raise StopIteration


for num in CountUp(5):
    print(num)


def my_generator(n):
    for i in range(n):
        yield i * i


for value in my_generator(5):
    print(value)


gen_exp = (x * 2 for x in range(5))

for val in gen_exp:
    print(val)