import math
import os

from Chart import Chart
from Rule import Rule

# The start symbol for the grammar
TOP = "TOP"

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
        # func probabilistic-CKY(words, grammar) returns most
        # probabilistic parse and its probability
        words = sentence
        grammar = self.ckyRules
        chart = Chart(sentence)

        # i: rows, j: cols
        for j in range(1, len(words)):
            for R in [grammar[k] for k in grammar if (words[j],) == grammar[k].children]:
                cell = chart.getCell(j - 1, j)
                cell.addItem(R.parent, R)  # P(A -> words[j])
            for i in reversed(range(j - 1)):
                for k in range(i + 1, j):
                    for R in grammar:
                        # Check if BinaryRule
                        # Check if table[i,j,B] > 0
                        # Check if table[i,j,C] > 0
                        # Check if table[i,j,A] < P (A -> BC) * table[i,j,B] * table[i,j,C]
                        # set table[i,j,A]
                        # set back[i,j,A] as {k, B, C}
                        pass

        TOP = chart.getRoot()
        # attach children
        return TOP




        # return InternalItem("Implement your CKY algorithm!", float('-inf'), ())


if __name__ == "__main__":
    pcfg = PCFG('../toygrammar.pcfg')
    sen = "the man eats the tuna with a fork and some sushi with the chopsticks".split()

    tree = pcfg.CKY(sen)
    if tree is not None:
        print(tree.toString())
        print("Probability: " + str(math.exp(tree.prob)))
        print("Num parses: " + str(tree.numParses))
    else:
        print("Parse failure!")
