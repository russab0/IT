from tools import NonAdaptiveCoder

INF = 10 ** 6


class Fano(NonAdaptiveCoder):

    def __init__(self, symbols, freq):
        self.symbols, self.freq = self.sort_by_freq(symbols, freq)
        self.codes = dict()
        self.fano(self.symbols, self.freq)

    def sort_by_freq(self, symbols, freq):
        new = list(zip(symbols, freq))
        new.sort(key=lambda x: -x[1])
        symbols, freq = zip(*new)
        return symbols, freq

    def fano(self, symbols, freq, cur_code=""):
        if len(symbols) == 1:
            self.codes[symbols[0]] = cur_code
            return
        min_delta = INF
        pos = 1
        for i in range(1, len(symbols)):
            cur_delta = abs(sum(freq[:i]) - sum(freq[i:]))
            if cur_delta < min_delta:
                min_delta = cur_delta
                pos = i
        self.fano(symbols[:pos], freq[:pos], cur_code + "0")
        self.fano(symbols[pos:], freq[pos:], cur_code + "1")


if __name__ == "__main__":
    # symbols = "ABCDEF"
    # freq = [0.4, 0.3, 0.1, 0.08, 0.07, 0.05]
    # codes = Fano(symbols, freq).codes
    tests = [
        # {'symbols': "abcde",
        # 'prob': [0.25, 0.25, 0.20, 0.15, 0.15],
        # 'text': "cde"},
        {'symbols': 'aeiou',
         'prob': [0.12, 0.42, 0.009, 0.30, 0.07],
         'text': 'iou'},
        {'symbols': 'abcd',
         'prob': [0.4, 0.3, 0.2, 0.1],
         'text': 'cab'}
    ]
    for test in tests:
        print(test)
        symbols = test['symbols']
        prob = test['prob']
        text = test['text']
        print(symbols, prob, text)
        fano = Fano(symbols, prob)
        print(fano.codes)
        print(fano.encode(text))
        print(fano.decode(fano.encode(text)))
