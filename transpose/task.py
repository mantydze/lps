import numpy as np

def worker(M):
    """ Transpose given matrix M
        M - 2D matrix
    """

    T = np.empty((M.shape[1], M.shape[0]), dtype='i')
    for x in range(M.shape[0]):
        for y in range(M.shape[1]):
            T[y][x] = M[x][y]
    return T