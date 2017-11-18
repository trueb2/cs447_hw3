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

    def __repr__(self):
        return "%s -> %s" % (self.parent, self.children())


'''
A UnaryRule has a probability, a parent category, and a child category/word
'''


class UnaryRule(Rule):
    def __init__(self, probability, parent, child):
        Rule.__init__(self, probability, parent)
        self.child = child

    # Returns a singleton (tuple) containing the rule's child
    def children(self):
        return self.child,  # note the comma; (self.child) is not a tuple


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
        return self.leftChild, self.rightChild


'''
An Item stores the label and Viterbi probability for a node in a parse tree
'''


class Item:
    def __init__(self, label, prob, numParses):
        self.label = label
        self.prob = prob
        self.numParses = numParses

    def __repr__(self):
        return self.toString()

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
        self.max_label = None
        self.max_prob = float('-inf')

    def addItem(self, item):
        if item.prob > self.max_prob:
            self.max_label = item.label
            self.max_prob = item.prob
        self.items[item.label] = item

    def getItem(self, label):
        return self.items[label]

    def getItems(self):
        return [self.items[label] for label in self.items]

    def getNumParses(self):
        return sum([self.items[label].numParses for label in self.items])

    def __repr__(self):
        return str(self.getItems())


'''
A Chart stores a Cell for every possible (contiguous) span of a sentence

Your task is to implement the stubs provided in this class
'''


class Chart:
    def __init__(self, sentence):
        # Initialize the chart, given a sentence
        self.chart = {}

        # Fill the chart with all the cells that we will need
        self.n = len(sentence)
        for i in range(self.n):
            for j in range(i, self.n):
                self.chart[(i, j)] = Cell()

        # Define the root
        self.root = (0, self.n - 1)

    def getRoot(self):
        return self.chart[self.root]

    def getCell(self, i, j):
        return self.chart[(i, j)]


'''
A PCFG stores grammatical rules (with probabilities), and can be used to
produce a Viterbi parse for a sentence if one exists
'''


class PCFG:
    def __init__(self, grammarFile, debug=False):
        # in ckyRules, keys are the rule's RHS (the rule's children, stored in
        # a tuple), and values are the parent categories
        self.ckyRules = {}
        self.debug = debug  # boolean flag for debugging
        # reads the probabilistic rules for this grammar
        self.readGrammar(grammarFile)
        # checks that the grammar at least matches the start symbol defined at
        # the beginning of this file (TOP)
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
                children = raw[3:]  # Note: here, children is a list; below, rule.children() is a tuple
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
        # Initialize a chart
        chart = Chart(sentence)

        # Fill the diagonals with words
        self.assign_diagonal(chart, sentence)

        # Iterate from left to right over columns
        for j in range(chart.n):  # j goes from 1 to n
            for i in reversed(range(j)):  # i goes from j-1 to 0
                # Get the target cell for these labels
                cell = chart.getCell(i, j)

                # Consider possible parses
                for k in range(i, j):
                    # Get B C productions from chart
                    left = chart.getCell(i, k)
                    right = chart.getCell(k+1, j)

                    # Consider all A where A -> left right
                    for leftItem in left.getItems():
                        for rightItem in right.getItems():
                            rhs = (leftItem.label, rightItem.label)
                            if rhs in self.ckyRules:
                                for rule in self.ckyRules[rhs]:
                                    internal_item = InternalItem(rule.parent, rule.prob + leftItem.prob + rightItem.prob)
                                    internal_item.numParses = leftItem.numParses * rightItem.numParses
                                    internal_item.children = (left, right, rule.children())
                                    cell.addItem(internal_item)

        # Each Item's children are the cells that could produce that InternalItem
        top_cell = chart.getRoot()
        top_item = top_cell.getItem(top_cell.max_label)
        productions = top_item.children[2]
        top_item.children = self.backtrack(top_item.children[0], productions[0]), self.backtrack(top_item.children[1], productions[1])
        TOP = InternalItem('TOP', top_item.prob, (top_item,))
        TOP.numParses = top_item.numParses

        return TOP #, top_item.prob, top_item.children

    def assign_diagonal(self, chart, sentence):
        """
        Fills the diagonal of the chart with the leaf items for each word in the sentence
        and the internal item for the word's production rule in the grammar

        :param chart:
        :param sentence:
        :return: None
        """
        for i, w in enumerate(sentence):
            cell = chart.getCell(i, i)

            # Add an InternalItem for the probability of producing word
            for rule in self.ckyRules[(w,)]:
                internal_item = InternalItem(rule.parent, rule.prob)
                internal_item.numParses = 1
                internal_item.children = LeafItem(w),
                cell.addItem(internal_item)

    def backtrack(self, cell, label):
        item = cell.getItem(label)
        if type(item.children[0]) != LeafItem:
            productions = item.children[2]
            item.children = self.backtrack(item.children[0], productions[0]), self.backtrack(item.children[1], productions[1])
        return item

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
