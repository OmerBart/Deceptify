import numpy as np


def bytes_to_array(b):
    # Determine the number of elements in the buffer based on the data type
    num_elements = len(b) // np.dtype(np.float64).itemsize

    if len(b) % np.dtype(np.float64).itemsize != 0:
        b = b[:num_elements * np.dtype(np.float64).itemsize]
    return np.frombuffer(b, dtype=np.float64)


def array_to_bytes(a):  # Converting a numpy array int byte-like array.
    return a.tobytes(order='C')
