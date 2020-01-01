from textwrap import wrap  # Allows to divide string into substring with equal lengths
from os import listdir  # List of files in the directory
from os.path import getsize  # Size of the given object

INPUT_DIR = 'dataset'  # directory in which original files are located
OUTPUT_DIR = 'RuslanSabirovOutputs'  # directory in which compressed and decompressed files would be places
FILE_TYPES = ['doc', 'pdf', 'jpg', 'png', 'exe']  # files are stored in corresponding folders


class LempelZiv:
    @staticmethod
    def gen_parent_byte(parent_id):
        """
        Converts integer id to the sequence of bytes
        (value of each byte’s first bit should indicate if it is the last byte (1) for ​i ​ or not (0))

        :param parent_id: integer id of the parent
        :return: id of the parent in the form of byte
        """
        parent_bin = bin(parent_id)[2:]  # Converting to binary
        if len(parent_bin) % 7 != 0:  # Adding leading zeros so that string would be dividable to substring of length 7
            parent_bin = (7 - len(parent_bin) % 7) * '0' + parent_bin
        parent_bin = wrap(parent_bin, 7)  # Divide string to substrings with length 7
        parent_bin = ["0" + x for x in parent_bin[:-1]] + ["1" + parent_bin[-1]]  # Marking last byte
        parent_byte = [bytes([int(x, 2)]) for x in parent_bin]  # Converting bits to bytes
        return parent_byte

    @staticmethod
    def get_parent_dec(parent_bin):
        """
        Converts sequence of bytes representing parent
        (value of each byte’s first bit should indicate if it is the last byte (1) for ​i ​ or not (0))
        to its integer representation

        :param parent_bin: sequence of bytes
        :return: integer value of parent id
        """
        parent_bin = [bin(x)[2:] for x in parent_bin]  # Converting bytes to bits
        parent_bin = [(8 - len(x)) * '0' + x for x in parent_bin]  # Adding leading zeros so that each group has 8 bits
        parent_bin = "".join([x[1:] for x in parent_bin])  # Cutting out first bit
        parent_id = int(parent_bin, 2)  # Converting sequence of bits to integer in decimal
        return parent_id

    def encode(self, input_file_loc, output_file_loc):
        file = open(input_file_loc, "rb")
        compressed = open(output_file_loc, "wb")
        size = getsize(file.name)  # size of the input file
        d = {b"": 0}  # Dictionary {byte: id_of_this_byte}
        cur = b""  # Current subsequence of bytes
        ind = 0  # Index of the subsequence
        i = 0  # Index of proceeding byte

        for x in file.read():  # For each byte
            cur += bytes([x])
            i += 1
            if cur not in d or i == size:  # If there is no such key in dict of if it is the last byte
                ind += 1
                parent_id = d[cur[:-1]]  # Cut of last byte of `cur` and get id of the parent from string
                parent_id_byte = self.gen_parent_byte(parent_id)  # Get byte representation of parent
                char_byte = bytes([cur[-1]])  # Current byte
                for b in parent_id_byte:
                    compressed.write(b)
                compressed.write(char_byte)
                d[cur] = ind  # Update dictionary
                cur = b""

        file.close()
        compressed.close()
        return output_file_loc

    def decode(self, input_file_loc, output_file_loc):
        file = open(input_file_loc, "rb")
        decompressed = open(output_file_loc, "wb")
        d = {0: b""}  # Dictionary {id_of_byte: byte_itself}
        i = 0  # Index of proceeding byte
        cur = []  # Current subsequence
        ind = 0  # Index of current subsequence
        last_byte = False  # Flag for determing whether the next byte will be about symbol

        for x in file.read():  # For each byte
            cur.append(x)
            if last_byte:  # If current byte represents symbol
                ind += 1
                parent_bin = cur[:-1].copy()  # All bytes except last
                parent_id = self.get_parent_dec(parent_bin)  # Convert to the decimal
                char = x

                d[ind] = d[parent_id] + bytes([char])  # Update the dict
                decompressed.write(d[ind])  # Write to the output file
                cur = list()
                last_byte = False
            elif x >= 128:  # This is the last byte representing parent
                last_byte = True
            else:
                i += 1

        file.close()
        decompressed.close()
        return output_file_loc


if __name__ == "__main__":
    LZ = LempelZiv()  # Object for performing compression and decompression on files

    all_ratios = dict()  # Dict of list of ratios for each file type

    for file_type in FILE_TYPES:  # Proceed through all types of files
        path = f"{INPUT_DIR}/{file_type}"  # Directory where all file of the proceeding file type are located  
        ratios = []  # List of rations of files of the proceeding file type

        for file in listdir(path):  # All files in the directory
            file_name, file_ext = file.split('.')
            original = f"{INPUT_DIR}/{file_type}/{file}"  # Location of original file
            compressed = f"{OUTPUT_DIR}/{file_type}/{file_name}Compressed.{file_ext}"  # Location of compressed file
            decompressed = f"{OUTPUT_DIR}/{file_type}/{file_name}Decompressed.{file_ext}"  # Location of decompressed
            # file

            LZ.encode(original, compressed)  # Compressing procedure
            LZ.decode(compressed, decompressed)  # Decompressing procedure

            original_size = getsize(original)  # Getting size of original file
            compressed_size = getsize(compressed)  # Getting size of compressed file
            decompressed_size = getsize(decompressed)  # Getting size of decompressed file
            assert original_size == decompressed_size

            comp_ratio = original_size / compressed_size  # Compression ration. Used in report
            ratios.append(comp_ratio)
            break

        all_ratios[file_type] = ratios
