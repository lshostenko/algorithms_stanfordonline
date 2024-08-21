import random
from copy import copy


def _swap(array, ix_1, ix_2):
    array[ix_1], array[ix_2] = array[ix_2], array[ix_1]


def _partition(array, i_min, i_max):
    i_p = random.randrange(i_min, i_max)
    pivot = array[i_p]

    _swap(array, i_p, i_min)

    i = i_min + 1
    j = i_min + 1

    while j < i_max and array[j] < pivot:
        i += 1
        j += 1

    while j < i_max:
        if array[j] < pivot:
            _swap(array, i, j)
            i += 1
        j += 1

    _swap(array, i_min, i - 1)

    return i - 1


def _rselect(array, i_min, i_max, order):
    if i_max - i_min < 2:
        return array[i_min]

    m = _partition(array, i_min, i_max)

    if m == order:
        return array[m]

    elif m < order:
        return _rselect(array, m + 1, i_max, order - m - 1)

    else:
        return _rselect(array, i_min, m, order)


def rselect(array, order):
    if not 0 <= order < len(array):
        raise ValueError('Incorrect value for \'order\' parameter.')

    return _rselect(copy(array), 0, len(array), order, pivot='random')
