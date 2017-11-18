'''
A Cell stores all of the parse tree nodes that share a common span

Your task is to implement the stubs provided in this class
'''


class Cell:

    def __init__(self):
        self.items = {}

    def addItem(self, rule):
        self.items[rule.parent] = rule
        pass

    def getItem(self, label):
        return self.items[label]

    def getItems(self):
        return [self.items[k] for k in self.items]
