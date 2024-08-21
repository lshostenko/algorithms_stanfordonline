import random
from copy import copy


def _swap(array, ix_1, ix_2):
    array[ix_1], array[ix_2] = array[ix_2], array[ix_1]


def _randpartition(array):
    i_p = random.randrange(len(array))
    pivot = array[i_p]

    _swap(array, i_p, 0)

    i_bound = 1
    swap = False

    for i in range(1, len(array)):
        if array[i] < pivot:
            if swap:
                _swap(array, i_bound, i)

            i_bound += 1
            continue

        swap = True

    _swap(array, 0, i_bound - 1)

    return i_bound - 1


def _rselect(array, order):
    if len(array) == 1:
        return array[0]

    m = _randpartition(array)

    if m == order:
        return array[m]

    elif m < order:
        return _rselect(array[m + 1:], order - m - 1)

    else:
        return _rselect(array[:m], order)


def rselect(array, order):
    if not 0 <= order < len(array):
        raise ValueError('Incorrect value for \'order\' parameter.')

    return _rselect(copy(array), order)
