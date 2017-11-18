import os
import math

# The start symbol for the grammar
TOP = "TOP"


class Rule:
    def __init__(self, A, BC, p):
        self.A = A
        assert (len(BC) == 1 or len(BC) == 2)
        self.BC = tuple(BC)
        self.p = p

    def __repr__(self):
        return "%s -> %s" % (self.A, self.BC)

class PCFG:
    def __init__(self, grammarFile):
        self.rules = []
        if os.path.isfile(grammarFile):
            file = open(grammarFile, "r")
            for line in file:
                raw = line.split()
                # reminder, we're using log probabilities
                prob = math.log(float(raw[0]))
                parent = raw[1]
                children = raw[3:]
                self.rules.append(Rule(parent, children, prob))

    '''
    Your task is to implement this method according to the specification. You may define helper methods as needed.

    Input:        sentence, a list of word strings
    Returns:      The root of the Viterbi parse tree, i.e. an InternalItem with label "TOP" whose probability is the Viterbi probability.
                   By recursing on the children of this node, we should be able to get the complete Viterbi tree.
                   If no such tree exists, return None\
    '''

    def CKY(self, sentence):
        """
        Ordering

        Fill Diagonal (0,0), (1,1), (2,2) ... (n,n)

        Fill Sub 1 Diagonal (0,1): [(0,0), (1,1)], (1,2): [(1,1), (2,2)], (1,2): ...

        Fill Sub 2 Diagonal (0,2): [{B:{0,0}, C:{1,2},{B:(1,0), C:(2,2)}], ...

        :param sentence:
        :return:
        """
        # Probabilistic CKY from textbook page 465
        words = sentence
        grammar = self.rules
        n = len(words)

        table = {}
        back = {}

        # Iterate over the columns left to right
        for j, w in enumerate(words):
            # Fill the diagonal based on the terminal word probabilities
            for r in grammar:
                if j == r.A:
                    table[(j, j, r.A)] = r.A
                    continue

            # Iterate over rows from the bottom up
            for i in reversed(range(j + 1)):
                for k in range(i+1, j):


            # Fail if a word is not in a terminal rule
            return None


        # Iterate over columns left to right
        for j in range(1, n + 1):

            # Set initial probabilities along word leaves
            for R in grammar:
                if (words[j-1],) == R.BC:
                    table[(j - 1, j, R.A)] = R.p
                    continue

            # Iterate up the rows from the bottom
            for i in reversed(range(j)):
                for k in range(i + 1, j):
                    for R in grammar:
                        if len(R.BC) == 1:
                            continue
                        k1 = (i, k, R.BC[0])
                        if k1 not in table:
                            continue
                        k2 = (k, j, R.BC[1])
                        if k2 not in table:
                            continue

                        kA = (i, j, R.A)
                        tA = R.p + table[k1] + table[k2]
                        if kA not in table:
                            table[kA] = tA
                            back[kA] = [{k, *R.BC}]
                        elif table[kA] < tA:
                            table[kA] = tA
                            back[kA].append({k, *R.BC})

        print(back)
        return None


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
