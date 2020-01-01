import numpy as np
from tools import NonAdaptiveCoder, dec_to_bin


class SFE(NonAdaptiveCoder):
    def __init__(self, symbols=None, prob=None):
        self.symbols = symbols
        self.prob = prob
        self.codes = dict()
        self.sfe()

    def sfe(self):
        cdf = np.cumsum(self.prob)
        mp = cdf - np.divide(self.prob, 2)

        lenght = np.ceil(- np.log2(self.prob) + 1)
        lenght = lenght.astype(int)
        mp_bin = [dec_to_bin(x)[2:] for x in mp]

        for i in range(len(mp_bin)):
            x = mp_bin[i]
            if lenght[i] <= len(x):
                code = x[:lenght[i]]
            else:
                code = x + "0" * (lenght[i] - len(x))
            char = self.symbols[i]
            self.codes[char] = code

    def decode_symbol(self, code):
        cdf = np.cumsum(self.prob)
        lower, upper = 0, 1
        for x in code:
            if x == "0":
                upper = (upper + lower) / 2
            else:
                lower = (upper + lower) / 2
        mid = (upper + lower) / 2
        index = 0
        while cdf[index] < mid:
            index += 1
        return self.symbols[index]


if __name__ == "__main__":
    # sfe = SFE("ABCDE", [0.25, 0.25, 0.20, 0.15, 0.15])
    # sfe = SFE("MATEKUDSI",
    #          [0.09090909090909091, 0.2727272727272727, 0.09090909090909091,
    #           0.09090909090909091, 0.09090909090909091, 0.09090909090909091,
    #           0.09090909090909091, 0.09090909090909091, 0.09090909090909091])
    sfe = SFE("ABCDEF", [0.25, 0.05, 0.2, 0.15, 0.1, 0.25])
    print(sfe.codes)
    #en = sfe.encode("BAD")
    #de = 
    print(sfe.decode_symbol("01000"))
    print("QU", sfe.decode("010000001100"))
