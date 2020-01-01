from queue import PriorityQueue
from tools import  NonAdaptiveCoder


class Tree:
    s = ""
    p = 0
    left = None
    right = None

    def __init__(self, s, prob, left=None, right=None):
        self.s = s
        self.p = prob
        self.left = left
        self.right = right

    def __le__(self, other):
        return self.p <= other.p

    def __lt__(self, other):
        return self.p < other.p

    def __str__(self):
        return f"Tree: s = `{self.s}`, prob = {self.p}"

    def is_leaf(self):
        return self.left is None and self.right is None

    def traverse(self, cur_code=""):
        if self.is_leaf():
            return {self.s: cur_code}

        left_codes = self.left.traverse(cur_code + "0")
        right_codes = self.right.traverse(cur_code + "1")
        return {**left_codes, **right_codes}


class Huffman(NonAdaptiveCoder):
    nodes = PriorityQueue()

    def __init__(self, symbols, freq):
        self.symbols = symbols
        self.freq = freq
        self.codes = dict()
        self.codes = self.huffman()

    def huffman(self):
        for s, p in zip(self.symbols, self.freq):
            node = Tree(s, p)
            self.nodes.put(node)

        while self.nodes.qsize() > 1:
            a = self.nodes.get()
            b = self.nodes.get()
            # print(a, b)
            new = Tree(a.s + b.s, a.p + b.p, a, b)
            self.nodes.put(new)
        root = self.nodes.get()

        return root.traverse()


if __name__ == "__main__":
    symbols = "ABCDEFGHI"
    freq = [0.05, 0.05, 0.25, 0.09, 0.30, 0.05, 0.03, 0.08, 0.1]
    codes = Huffman(symbols, freq).codes
    print(codes)
    #print(list(zip(codes)))
    #print(sorted(list(codes), key=lambda x: x[0]))
