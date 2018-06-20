def worker(M):
    """ M - 3D matrix
    """
    _min = M[0][0][0]
    _max = M[0][0][0]

    for x in range(M.shape[0]):
        for y in range(M.shape[1]):
            for z in range(M.shape[2]):

                if M[x][y][z] < _min:
                    _min = M[x][y][z]

                if M[x][y][z] > _max:
                    _max = M[x][y][z]

    result = {
        "_min": _min,
        "_max": _max
    }
    return result