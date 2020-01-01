import numpy as np
from os import listdir
from os.path import isfile, join

BASE_DIR = 'dataset'  # all folders with the same file types are stored in this directory
FILE_TYPES = ['doc', 'pdf', 'exe', 'jpg', 'png']  # files are stored in corresponding folders


def calculate_entropy(file_dir):
    """
    Calculates Shannon Entropy for the given file
    :param file_dir: location of the file
    :return: Shannon Entropy of the file
    """

    file = open(file_dir, "rb")  # Open in mode for reading bytes
    cnt = np.zeros((256,))  # Array for counting frequencies
    for byte in file.read():  # Calculating frequencies of bytes
        cnt[byte] += 1

    cnt = cnt[cnt > 0]  # Lefts only bytes that has been appeared at least once
    prob = cnt / np.sum(cnt)  # Calculate probabilities
    entropy = -np.dot(prob, np.log2(prob))  # Calculates entropy sum of multiplications is actually dot product
    file.close()  # Close the file
    return entropy


if __name__ == "__main__":
    # Creating dictionaries for storing statistical data about entropies
    res_avg = dict()
    res_var = dict()
    res_max = dict()
    res_min = dict()
    all_entropies = np.array([])

    for file_type in FILE_TYPES:  # Proceed through all types of files
        path = f"{BASE_DIR}/{file_type}"  # Create string for path of the folder
        files = listdir(path)  # All files in the directory

        entropies = np.array([calculate_entropy(f'{path}/{file}') for file in files])  # Calculate entropy for all files
        all_entropies = np.concatenate([all_entropies, entropies])  # Add all these entopies to common array

        # Store the statisctics for current file type
        res_avg[path] = entropies.mean()
        res_var[path] = entropies.var()
        res_max[path] = entropies.max()
        res_min[path] = entropies.min()
        print(path, entropies.mean())

    # Compute statistics for all entropies
    res_avg['all'] = all_entropies.mean()
    res_var['all'] = all_entropies.var()
    res_max['all'] = all_entropies.max()
    res_min['all'] = all_entropies.min()

    for x in res_avg:  # Print all results
        print(f"File type: {x}, var: {res_var[x]}, min: {res_min[x]}, avg: {res_avg[x]}, max: {res_max[x]}")

