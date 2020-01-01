import os
import matplotlib
import matplotlib.pyplot as plt

np = matplotlib.numpy  # for matrix operations
INPUT_DIR = 'inputs'
OUTPUT_DIR = 'RuslanSabirovOutputs'
DFT_MIN_SIZE = 8
QUALITY_SAVE_RATE = 0.1  # Should be in the range [0; 1]


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140]).astype('uint8')


def DFT1d(arr, inverse=False):
    """
    Calculates Discrete Fourier Transform of the 1D array x in slow manner
    :param arr: 1d numpy-array
    :param inverse: True if inverse DFT needed
    :return: 1d numpy-array, result of performed DFT
    """

    N = arr.shape[0]
    assert len(arr.shape) == 1, "DFT1d is only for 1-dimensional FFT"
    assert N & (N - 1) == 0, "Array size should be the power of 2"

    n = np.arange(0, N)  # list of integers from range [0; N)
    k = n[:, None]  # each number is located on separate row
    if not inverse:
        w = np.exp(-2j * np.pi * k * n / N)
    else:
        w = np.exp(+2j * np.pi * k * n / N)
    ans = np.dot(w, arr)  # multiplication on two matrices

    return ans


def FFT1d(arr, inverse=False, N_init=None):
    """
    Calculates Fast Fourier Transform of the 1D array using Cooley-Turkey algorithm
    :param arr: 1d numpy-array
    :param inverse: True if inverse FFT needed (False by default)
    :param N_init: variable for internal purposes, should be None when calling outside this function
    :return: 1d numpy-array, result of performed FFT
    """

    N = arr.shape[0]
    assert len(arr.shape) == 1, "FFT1d is only for 1-dimensional FFT"
    assert N & (N - 1) == 0, "Array size should be the power of 2"

    if N_init is None:  # means that this is top level of recursion
        N_init = N  # fixing the size of array at the top level of recursion

    if N <= DFT_MIN_SIZE:  # recursion base case: array size is to big to perform recursion
        return DFT1d(arr, inverse)

    arr_even = FFT1d(arr[0::2], inverse=inverse, N_init=N_init)  # FFT1d on array elements with even indexes
    arr_odd = FFT1d(arr[1::2], inverse=inverse, N_init=N_init)  # FFT1d on array elements with odd indexes

    if not inverse:
        w = np.exp(-2j * np.pi * np.arange(N) / N)
    else:
        w = np.exp(+2j * np.pi * np.arange(N) / N)

    first_part = arr_even + w[:N // 2] * arr_odd  # first half of coefficients
    second_part = arr_even + w[N // 2:] * arr_odd  # second half of coefficients
    ans = np.concatenate([first_part, second_part])  # concatenating two halfs

    if inverse and N_init == N:  # we need to normalize only if it top-level of inverse function
        ans /= N

    return ans


def FFT2d(img, inverse=False):
    """
    Calculates Fast Fourier Transform of the 2D array using FFT1d
    :param img: numpy-array, image
    :param inverse: True if inverse FFT needed (False by default)
    :return: 2d numpy-array, result of performed FFT
    """
    N, M = img.shape
    assert len(img.shape) == 2, "FFT2d is only for 2d images"
    assert N & (N - 1) == 0, "Each side should be the power of 2"
    assert M & (M - 1) == 0, "Each side should be the power of 2"

    # Perform FFT1d on each row
    img = np.asarray(img, dtype='complex')
    for i in range(img.shape[0]):
        img[i] = FFT1d(img[i], inverse=inverse)

    # Perform FFT1d on each column
    img = img.T  # Columns became rows
    for i in range(img.shape[0]):
        img[i] = FFT1d(img[i], inverse=inverse)
    img = img.T  # Columns returned on the right place
    return img


def compress(arr):
    """
    Set some items of the given array to zero so that rate of the saved items would be less than QUALITY_SAVE_RATE.
    Uses ternary search to perform search on convex function abs().
    :param arr: array to perform cut-off
    :return: resulting array
    """
    arr = arr.copy()
    n, m = arr.shape
    to_reset = int((1 - QUALITY_SAVE_RATE) * n * m)

    left, right = arr.min(), arr.max()  # borders for threshold
    while right - left > 1:
        # divide (l, r] into three parts: (l, m1], (m1, m2], (m2, r]
        mid1 = left + (right - left) / 3
        mid2 = right - (right - left) / 3

        cnt1 = np.count_nonzero((abs(arr) < mid1) == True)  # number of items which abs value less than threshold
        cnt2 = np.count_nonzero((abs(arr) < mid2) == True)  # number of items which abs value less than threshold

        if cnt2 >= cnt1 and cnt2 >= to_reset:
            right = mid2
        else:
            left = mid1

    threshold = right  # final threshold
    # cnt = np.count_nonzero((abs(arr) < threshold) == True)
    # print(threshold, cnt, to_reset)  # used to check
    arr[(abs(arr) < threshold)] = 0  # reset items to 0
    return arr


def main():
    assert INPUT_DIR in os.listdir(), "No input directory"
    if OUTPUT_DIR not in os.listdir():
        os.mkdir(OUTPUT_DIR)

    files = os.listdir(INPUT_DIR)
    for filename in files:  # for each file
        img = plt.imread(f"{INPUT_DIR}/{filename}", format='tiff')  # read in RGB format
        if len(img.shape) > 2:  # if has more that one channel
            img = img[..., 0]  # each channel of the pixel is the same, we can left only one of them

        fft = FFT2d(img)  # perform FFT
        compressed = compress(fft)  # remove some resulting values by the threshold
        decompressed = FFT2d(compressed, inverse=True)  # perform InverseFFT under result of the FFT and cut-off

        name, ext = filename.split(".")  # extract name of the file and its extension
        plt.imsave(f"{OUTPUT_DIR}/{name}Compressed.{ext}",  # Saving image to the ouput folder
                   decompressed.astype(int),  # cut off the imaginary part
                   format='tiff',  # specify the format
                   cmap=plt.get_cmap('gray'))  # save ing the grayscale


from time import time

a = time()
main()
b = time()
# print(b - a)
