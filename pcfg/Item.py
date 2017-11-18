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
