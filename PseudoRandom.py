class PseudoRandom:
    def __init__(self, seed=0, m=2**32, a=1103515245, c=12345, listMode = False, rndList = []):
        self.seed = seed
        self.m = m
        self.a = a
        self.c = c
        self.listMode = listMode
        self.rndList = rndList

    def rand(self):
        if self.listMode and self.rndList != []:
            return self.rndList.pop(0)

        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed / self.m

    def range(self, a, b):
        return (b - a) * self.rand() + a
    
    def get_rndList(self):
        return self.rndList