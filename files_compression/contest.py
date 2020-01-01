import sys


def validate(filename1: str, filename2: str):
    try:
        with open(filename1, 'rb') as file1:
            with open(filename2, 'rb') as file2:
                for byte1, byte2 in zip(file1, file2):
                    if byte1 != byte2:
                        return False
                return True
    except FileNotFoundError as error:
        return error


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Not enought files to compare: expect 2')
    elif len(sys.argv) > 3:
        print('Too much files to compare: expect 2')
    else:
        print(validate(sys.argv[1], sys.argv[2]))
