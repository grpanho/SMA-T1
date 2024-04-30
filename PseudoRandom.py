class PseudoRandom:
    def __init__(self, seed, m=2**32, a=1103515245, c=12345):
        self.seed = seed
        self.m = m
        self.a = a
        self.c = c

    def rand(self):
            self.seed = (self.a * self.seed + self.c) % self.m

            return self.seed / self.m

    def range(self, a, b):
        return (b - a) * self.rand() + a