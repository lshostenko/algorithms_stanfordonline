import gzip
import random
from copy import copy


def _swap(array, ix_1, ix_2):
    array[ix_1], array[ix_2] = array[ix_2], array[ix_1]


def _partition(array, i_min, i_max, count, pivot='first'):
    if pivot == 'first':
        i_p = i_min
        pivot = array[i_p]

    elif pivot == 'last':
        i_p = i_max - 1
        pivot = array[i_p]

    elif pivot == 'median':
        ixs = (i_min, i_min + (i_max - i_min - 1) // 2, i_max - 1)
        pivot, i_p = sorted((array[i], i) for i in ixs)[1]

    elif pivot == 'random':
        i_p = random.randrange(i_min, i_max)
        pivot = array[i_p]

    elif pivot == 'random_3':
        ixs = (random.randrange(i_min, i_max) for _ in range(3))
        pivot, i_p = sorted((array[i], i) for i in ixs)[1]

    elif pivot == 'random_5':
        ixs = (random.randrange(i_min, i_max) for _ in range(5))
        pivot, i_p = sorted((array[i], i) for i in ixs)[2]

    else:
        raise ValueError('\'pivot\' value is not allowed.')

    _swap(array, i_p, i_min)

    i_bound = i_min + 1
    swap = False

    for i in range(i_min + 1, i_max):
        if array[i] < pivot:
            if swap:
                _swap(array, i_bound, i)

            i_bound += 1
            continue

        swap = True

    _swap(array, i_min, i_bound - 1)

    return i_bound - 1, count + i_max - i_min - 1


def _quicksort(array, i_min, i_max, count, pivot='first'):
    if i_max - i_min > 1:
        m, count = _partition(array, i_min, i_max, count, pivot=pivot)
        count = _quicksort(array, i_min, m, count, pivot=pivot)
        count = _quicksort(array, m + 1, i_max, count, pivot=pivot)

    return count


def quicksort(array, pivot='first'):
    """Sorts 'array' in place and returns number of comparisons."""
    return _quicksort(array, 0, len(array), 0, pivot=pivot)


# Programming Assignment 2
if __name__ == '__main__':
    with gzip.open('assets/QuickSort.txt.gz', mode='rt') as fp:
        array = [int(i) for i in fp.read().split()]

    for pivot in ['first', 'last', 'median']:
        comparisons = quicksort(copy(array), pivot=pivot)
        print(f'pivot=\'{pivot}\':\t{comparisons}')
