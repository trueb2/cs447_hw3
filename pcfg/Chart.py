'''
A Chart stores a Cell for every possible (contiguous) span of a sentence

Your task is to implement the stubs provided in this class
'''
from Cell import Cell


class Chart:

    def __init__(self, sentence):
        # Initialize the chart, given a sentence
        self.index = {}
        n = len(sentence)+1
        self.TOP = (n-1,n-1)
        for i in range(n+1):
            for j in range(i,n+1):
                self.index[(i,j)] = Cell()


    def getRoot(self):
        # Return the item from the top cell in the chart with
        # the label TOP
        return self.index[self.TOP]

    def getCell(self, i, j):
        # Return the chart cell at position i, j
        return self.index[(i,j)]
