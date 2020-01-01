import SFE
import fano
import huffman
import arithmetic


def calc_exp_len(symbols, freq, codes):
    if not codes:
        return None
    exp_len = 0
    for i in range(len(symbols)):
        s = symbols[i]
        p = freq[i]
        exp_len += p * len(codes[s])
    return exp_len


algorithms = [#("Fano", fano.Fano),
              ("Huffman", huffman.Huffman),
              #("SFE", SFE.SFE),
              #("Arithmetic", arithmetic.Arithmetic)
              ]

tests = [
    #{'symbols': "abcdef",
    #'prob': [0.25, 0.05, 0.2, 0.15, 0.1, 0.25],
    #'text': 'abcdef'},
    {
        'symbols': "ABCDEFGHI",
        'prob': [0.05, 0.05, 0.25, 0.09, 0.30, 0.05, 0.03, 0.08, 0.1],
        'text': 'AB'
    }
]
"""{'symbols': "abcde",
     'prob': [0.25, 0.25, 0.20, 0.15, 0.15],
     'text': "cde"},
    {'symbols': 'aeiou',
     'prob': [0.12, 0.42, 0.009, 0.30, 0.07],
     'text': 'iou'},
    {'symbols': 'abcd',
     'prob': [0.4, 0.3, 0.2, 0.1],
     'text': 'cab'},
    {'symbols': "abcdef",
     'prob': [0.4, 0.3, 0.1, 0.08, 0.07, 0.05],
     'text': 'dab'},
    {'symbols': "abcde",
     'prob': [0.4, 0.2, 0.2, 0.1, 0.1],
     'text': 'bad'},
    {'symbols': "cba",
     'prob': [0.2, 0.4, 0.4],
     'text': 'cab'}""" 
    
for test in tests:
    print("TEST", test)
    symbols = test['symbols']
    prob = test['prob']
    text = test['text']

    for name, cls in algorithms:
        obj = cls(symbols, prob)
        codes = obj.codes
        exp_len = calc_exp_len(symbols, prob, codes)

        print(name, exp_len)
    print()

    for name, cls in algorithms:
        obj = cls(symbols, prob)
        encoded = obj.encode(text)
        if name == 'Arithmetic':
            decoded = obj.decode(encoded, len(text))
        else:
            decoded = obj.decode(encoded)
        print(name, encoded, len(encoded), decoded)
    print("\n" + "-" * 10)
