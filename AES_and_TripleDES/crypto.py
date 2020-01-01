from Crypto.Cipher import DES3, AES


def main(cls, block):
    def pad(text):
        bytes_to_add = (block - len(text) % block) % block
        text = text + b' ' * bytes_to_add
        return text

    def encrypt(text, key):
        padded_text = pad(text)
        des = cls.new(key, cls.MODE_ECB)
        return des.encrypt(padded_text)

    def decrypt(text, key):
        des = cls.new(key, cls.MODE_ECB)
        return des.decrypt(text)

    def check(text1, text2):
        return pad(text1) == pad(text2)

    key = b'abcdefghijklmnop'
    fin = open("input.txt", "rb")
    text = fin.read()
    encrypted = encrypt(text, key)
    decrypted = decrypt(encrypted, key)

    class_name = cls.__name__.split('.')[-1]
    out_filename = f"output{class_name}.txt"
    fout = open(out_filename, "wb")
    fout.write(decrypted)
    fout.close()

    fout = open(out_filename, "rb")
    text_out = fout.read()
    print(class_name, check(text, text_out))


main(DES3, 8)
main(AES, 16)
