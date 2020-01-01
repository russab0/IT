from math import modf

EPS = 1e-9
MAX_LENGHT = 30


def fractional_part(num):
    return modf(num)[0]


def dec_to_bin(num):
    ans = str()
    i = 0
    while i < MAX_LENGHT and fractional_part(num) > EPS:
        num *= 2
        if num >= 1:
            ans += "1"
        else:
            ans += "0"

        num -= int(num)
        i += 1
    return "0." + ans


def bin_to_dec(num):
    ans = 0
    for i in range(len(num)):
        x = num[i]
        if x == "1":
            ans += 2 ** (-i - 1)
    return ans


class NonAdaptiveCoder:
    codes = dict()
    codes_inverse = None

    def encode(self, text):
        text = text.lower()
        ans = ""
        for x in text:
            ans += self.codes[x] + ""
        return ans

    def decode(self, message):
        if self.codes_inverse is None:
            self.codes_inverse = dict(zip(self.codes.values(), self.codes.keys()))
        substr = ""
        ans = ""
        #print(self.codes_inverse)
        #print(message)
        for x in message:
            substr += x
            if substr in self.codes_inverse:
                ans += self.codes_inverse[substr]
                substr = ""
            #print(substr, ans)
        return ans
