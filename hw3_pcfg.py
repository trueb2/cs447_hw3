import sys
import os
import math

# The start symbol for the grammar
TOP = "TOP"

'''
A grammatical Rule has a probability and a parent category, and is
extended by UnaryRule and BinaryRule
'''


class Rule:

    def __init__(self, probability, parent):
        self.prob = probability
        self.parent = parent

    # Factory method for making unary or binary rules (returns None otherwise)
    @staticmethod
    def createRule(probability, parent, childList):
        if len(childList) == 1:
            return UnaryRule(probability, parent, childList[0])
        elif len(childList) == 2:
            return BinaryRule(probability, parent, childList[0], childList[1])
        return None

    # Returns a tuple containing the rule's children
    def children(self):
        return ()

'''
A UnaryRule has a probability, a parent category, and a child category/word
'''


class UnaryRule(Rule):

    def __init__(self, probability, parent, child):
        Rule.__init__(self, probability, parent)
        self.child = child

    # Returns a singleton (tuple) containing the rule's child
    def children(self):
        return (self.child,)  # note the comma; (self.child) is not a tuple

'''
A BinaryRule has a probability, a parent category, and two children
'''


class BinaryRule(Rule):

    def __init__(self, probability, parent, leftChild, rightChild):
        Rule.__init__(self, probability, parent)
        self.leftChild = leftChild
        self.rightChild = rightChild

    # Returns a pair (tuple) containing the rule's children
    def children(self):
        return (self.leftChild, self.rightChild)

'''
An Item stores the label and Viterbi probability for a node in a parse tree
'''


class Item:

    def __init__(self, label, prob, numParses):
        self.label = label
        self.prob = prob
        self.numParses = numParses

    # Returns the node's label
    def toString(self):
        return self.label

'''
A LeafItem is an Item that represents a leaf (word) in the parse tree (ie, it
doesn't have children, and it has a Viterbi probability of 1.0)
'''


class LeafItem(Item):

    def __init__(self, word):
        # using log probabilities, this is the default value (0.0 = log(1.0))
        Item.__init__(self, word, 0.0, 1)

'''
An InternalNode stores an internal node in a parse tree (ie, it also
stores pointers to the node's child[ren])
'''


class InternalItem(Item):

    def __init__(self, category, prob, children=()):
        Item.__init__(self, category, prob, 0)
        self.children = children
        # Your task is to update the number of parses for this InternalItem
        # to reflect how many possible parses are rooted at this label
        # for the string spanned by this item in a chart
        self.numParses = -1  # dummy numParses value; this should not be -1!
        if len(self.children) > 2:
            print("Warning: adding a node with more than two children (CKY may not work correctly)")

    # For an internal node, we want to recurse through the labels of the
    # subtree rooted at this node
    def toString(self):
        ret = "( " + self.label + " "
        for child in self.children:
            ret += child.toString() + " "
        return ret + ")"

'''
A Cell stores all of the parse tree nodes that share a common span

Your task is to implement the stubs provided in this class
'''


class Cell:

    def __init__(self):
        self.items = {}

    def addItem(self, item):
        self.items[item.label] = item

    def getItem(self, label):
        return self.items[item.label]

    def getItems(self):
        return [self.items[label] for label in self.items]

'''
A Chart stores a Cell for every possible (contiguous) span of a sentence

Your task is to implement the stubs provided in this class
'''


class Chart:

    def __init__(self, sentence):
        self.cells = {}
        self.n = len(sentence)
        self.S = (self.n, self.n)
        for i in range(self.n + 1):
            for j in range(self.n + 1):
                self.cells[(i,j)] = Cell()

    def getRoot(self):
        return self.cells[self.S]

    def getCell(self, i, j):
        return self.cells[(i,j)]

'''
A PCFG stores grammatical rules (with probabilities), and can be used to
produce a Viterbi parse for a sentence if one exists
'''


class PCFG:

    def __init__(self, grammarFile, debug=False):
        self.ckyRules = {}
        self.debug = debug
        self.readGrammar(grammarFile)
        self.topCheck()

    '''
    Reads the rules for this grammar from an input file
    '''

    def readGrammar(self, grammarFile):
        if os.path.isfile(grammarFile):
            file = open(grammarFile, "r")
            for line in file:
                raw = line.split()
                # reminder, we're using log probabilities
                prob = math.log(float(raw[0]))
                parent = raw[1]
                children = raw[3:]
                rule = Rule.createRule(prob, parent, children)
                if rule.children() not in self.ckyRules:
                    self.ckyRules[rule.children()] = set([])
                self.ckyRules[rule.children()].add(rule)

    '''
    Checks that the grammar at least matches the start symbol (TOP)
    '''

    def topCheck(self):
        for rhs in self.ckyRules:
            for rule in self.ckyRules[rhs]:
                if rule.parent == TOP:
                    return  # TOP generates at least one other symbol
        if self.debug:
            print("Warning: TOP symbol does not generate any children (grammar will always fail)")

    '''
    Your task is to implement this method according to the specification. You may define helper methods as needed.

    Input:        sentence, a list of word strings
    Returns:      The root of the Viterbi parse tree, i.e. an InternalItem with label "TOP" whose probability is the Viterbi probability.
                   By recursing on the children of this node, we should be able to get the complete Viterbi tree.
                   If no such tree exists, return None\
    '''

    def CKY(self, sentence):
        # func probabilistic-CKY(words, grammar) returns most
        # probabilistic parse and its probability
        words = sentence
        grammar = self.ckyRules
        chart = Chart(sentence)
        back = {}

        # i: rows, j: cols
        for j in range(1, len(words)):
            # Fill leaves on diagonals
            for k in grammar:
                if (words[j],) == grammar[k].children:
                    char.getCell(j-1,j).addItem(LeftItem(words[j]))
            # Move right through the columns and Up through the rows
            for i in reversed(range(j - 2)):
                for k in range(i + 1, j):
                    for R in grammar:
                        # Check if BinaryRule
                        if type(R) is UnaryRule:
                            continue

                        # Check if table[i,k,B] > 0
                        B_cell = chart.getCell(i,k)
                        t_B = B_cell.getItem(R.children[0]).prob
                        if t_B == float('-inf'):
                            continue

                        # Check if table[k,j,C] > 0
                        C_cell = chart.getCell(k,j)
                        t_C = C_cell.getItem(R.children[1]).prob
                        if t_C == float('-inf'):
                            continue

                        # Check if table[i,j,A] < P (A -> BC) * table[i,j,B] * table[i,j,C]
                        A_cell = chart.getCell(i,j)
                        item = A_cell.getItem(R.parent)
                        t_A_ = math.log(R.prob) + t_B + t_C
                        if item.prob < t_A_:
                            item.prob = t_A_
                            back[(i,j,R.parent)] = (k, *R.children)

        print(back)
        return TOP


if __name__ == "__main__":
    pcfg = PCFG('toygrammar.pcfg')
    sen = "the man eats the tuna with a fork and some sushi with the chopsticks".split()

    tree = pcfg.CKY(sen)
    if tree is not None:
        print(tree.toString())
        print("Probability: " + str(math.exp(tree.prob)))
        print("Num parses: " + str(tree.numParses))
    else:
        print("Parse failure!")
