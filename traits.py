class Traits():
    def __init__(self, strength: int = 0, endurance: int = 0, technical : int = 0, mentality: int = 0):
        self.s = strength
        self.e = endurance
        self.t = technical
        self.m = mentality

    def list(self):
        return [self.s, self.e, self.t, self.m]
    
    def __add__(self, other):
        return Traits(*[s + o for s, o in zip(self.list(), other.list())])