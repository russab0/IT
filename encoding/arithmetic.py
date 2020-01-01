import numpy as np
from tools import dec_to_bin, bin_to_dec


class Arithmetic:
    codes = None

    def __init__(self, symbols, prob):
        self.symbols = symbols
        self.prob = prob
        self.cdf = np.cumsum(self.prob)

    def encode(self, text):
        lower, upper = 0, 1
        cdf = self.cdf

        for x in text:
            index = self.symbols.find(x)
            delta = upper - lower

            upper = lower + delta * cdf[index]
            if index != 0:
                lower = lower + delta * cdf[index - 1]
            else:
                pass #lower = lower + delta * lower
            if abs(lower - upper) < 1e-6:
                break
        print("final", lower, upper)
        lower_bin = dec_to_bin(lower)
        upper_bin = dec_to_bin(upper)
        print("final", lower_bin, upper_bin)
        ans = ""

        for i in range(2, min(len(lower_bin), len(upper_bin))):
            ans += upper_bin[i]
            if lower_bin[i] != upper_bin[i]:
                break
        return ans

    def decode(self, message, size=100):
        code = float(bin_to_dec(message))
        lower, upper = 0, 1
        ans = ""
        i = 0
        while i < size:
            i += 1
            delta = upper - lower

            index = 0
            while lower + delta * self.cdf[index] < code:
                index += 1
            ans += self.symbols[index]
            upper = lower + delta * self.cdf[index]
            if index != 0:
                lower = lower + delta * self.cdf[index - 1]
            else:
                pass#lower = lower + delta * lower
        return ans


if __name__ == "__main__":
    # ar = Arithmetic("aeiou", [0.12, 0.42, 0.09, 0.30, 0.07])
    # print(ar.encode("iou"))
    ar = Arithmetic("abcd"[::-1], [0.5, 0.2, 0.25, 0.05][::-1])
    print(ar.encode("abc"))
    #print(ar.decode("00101", 3))
