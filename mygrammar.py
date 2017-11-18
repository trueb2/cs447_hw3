from collections import defaultdict


LEX = {
    "COMMA": set([","]),
    "FS": set(["."]),
    "CC": set(["And",  "But",  "and", "but"]),
    "CD": set(["1929",  "66.5",  "69"]),
    "DT": set(["All",  "No",  "The",  "a",  "no",  "the"]),
    "EX": set(["There"]),
    "IN": set(["after",  "by",  "for",  "from",  "in",  "into",  "of",  "on",  "that", "despite"]),
    "JJ": set(["crude",  "different",  "funny",  "high-priced",  "imaginative",  "immediate",  "many",  "moderate",  "nervous",  "new",  "worst-case", "political", "overwhelming"]),
    "MD": set(["can"]),
    "NN": set(["Champagne",  "Factory",  "PC",  "Stock",  "asbestos",  "bearing",  "breakdown",  "business",  "crash",  "dessert",  "face",  "field",  "force",  "lion",  "nose",  "oblivion",  "pioneer",  "predecessor",  "pressure",  "price",  "production",  "rest",  "scenario",  "share",  "today",  "work",   "trading", "president"]),
    "NNP": set(["Baltimore",  "Barnum",  "Courter",  "Cray",  "Dugdale",  "Esso",  "France",  "Hong",  "Kong",  "Korea",  "Learning",  "Mr.",  "Research",  "September",  "South",  "Tuesday",  "VanSant",  "Viacom",  "Whiting"]),
    "NNPS": set(["Materials"]),
    "NNS": set(["Pressures",  "Terms",  "banks",  "bottles",  "computers",  "concerns",  "contributors",  "investors",  "payrolls",  "prices",  "products",  "shares",  "ships",  "standards",  "subskills",  "tactics"]),
    "POS": set(["'s"]),
    "PRP": set(["It",  "They",  "it"]),
    "PRPX": set(["Her",  "our"]),
    "RB": set(["fractionally",  "n't",  "now",  "often"]),
    "TO": set(["to"]),
    "VB": set(["boast",  "build", "agree"]),
    "VBD": set(["began",  "called",  "came",  "fell",  "followed",  "had",  "matched",  "rose",  "said",  "started",  "suffered",  "went",  "were", "understood", "did"]),
    "VBG": set([ "using"]),
    "VBN": set(["been",  "disclosed",  "handled",  "set"]),
    "VBP": set(["operate"]),
    "VBZ": set(["'s",  "denies",  "grows",  "has",  "is"])
}


if __name__ == "__main__":
    print(LEX)

    states = []
    with open('sentences.txt', 'r') as f:
        for line in f:
            words = line[:-1].split(' ')
            tagged = []
            for word in words:
                tags = []
                for tag in LEX:
                    if word in LEX[tag]:
                        tags.append(tag)
                tagged.append(tags)

            taggings = ['']
            for tags in tagged:
                acc = []
                for tag in tags:
                    for t in taggings:
                        acc.append(t + " " + tag)
                if len(acc) != 0:
                    taggings = acc

            print(words)
            print(taggings)
            for tagging in taggings:
                states.append(tagging)

    print("//////////////")

    print(states)
    bigrams = defaultdict(int)
    for seq in states:
        seq = seq.split(" ")
        for i in range(1, len(seq)):
            if seq[i-1] == '':
                continue
            bigrams[(seq[i-1], seq[i])] += 1

    print("//////////////")
    print(bigrams)

    c = defaultdict(set)
    for a, b in bigrams:
        c[a].add(b)
    print(c)
