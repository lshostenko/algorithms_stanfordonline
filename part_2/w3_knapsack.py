import gzip
import sys
from time import monotonic
from functools import cache

import numpy as np

sys.setrecursionlimit(2 ** 16)


def _calculate_table(capacity, weights, values):
    _check_args(capacity, weights, values)

    dtype = np.min_scalar_type(sum(values))
    num_items = len(values)

    table = np.empty((num_items + 1, capacity + 1), dtype=dtype)
    table[0, :] = 0
    table[:, 0] = 0

    for i in range(1, num_items + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]

        if w_i >= capacity + 1:
            table[i] = table[i - 1]
            continue

        table[i, :w_i] = table[i - 1, :w_i]
        table[i, w_i:] = np.maximum(
            table[i - 1, w_i:],
            table[i - 1, :capacity + 1 - w_i] + v_i,
        )

    return table


def _check_args(capacity, weights, values):
    if not isinstance(capacity, int):
        raise ValueError('\'capacity\' should be integer.')

    if len(weights) != len(values):
        raise ValueError('\'weights\' and \'values\' should have equal size.')

    if not all(isinstance(w, int) and w > 0 for w in weights):
        raise ValueError('\'weights\' items should be positive integers.')

    if not all(v >= 0 for v in values):
        raise ValueError('\'values\' items should be non-negative.')


def knapsack(capacity, weights, values):
    table = _calculate_table(capacity, weights, values)
    num_items = len(values)

    max_value = table[num_items, capacity].item()

    ixs = []
    j = capacity

    for i in range(num_items, 0, -1):
        if table[i, j] != table[i - 1, j]:
            ixs.append(i - 1)
            j -= weights[i - 1]

    return max_value, tuple(ixs[::-1])


def knapsack_max_value(capacity, weights, values):
    _check_args(capacity, weights, values)

    dtype = np.min_scalar_type(sum(values))
    num_items = len(values)
    cur_row = np.zeros(capacity + 1, dtype=dtype)

    for i in range(1, num_items + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]

        if w_i >= capacity + 1:
            continue

        next_row = np.zeros_like(cur_row)
        next_row[:w_i] = cur_row[:w_i]
        next_row[w_i:] = np.maximum(
            cur_row[w_i:],
            cur_row[:capacity - w_i + 1] + v_i,
        )

        cur_row = next_row

    return cur_row[capacity].item()


def knapsack_max_value_recursive(capacity, weights, values):
    _check_args(capacity, weights, values)

    @cache
    def _knapsack(size, ix):
        if size == 0 or ix == 0:
            return 0

        if size < weights[ix - 1]:
            value = _knapsack(size, ix - 1)

        else:
            value = max(
                _knapsack(size, ix - 1),
                _knapsack(size - weights[ix - 1], ix - 1) + values[ix - 1],
            )

        return value

    return _knapsack(capacity, len(values))


def load_data(filename):
    weights = []
    values = []

    if filename.endswith('.gz'):
        open_file = gzip.open
    else:
        open_file = open

    with open_file(filename, mode='rt') as fp:
        capacity, n_items = map(int, fp.readline().split())

        for line in fp.readlines():
            v, w = map(int, line.split())
            weights.append(w)
            values.append(v)

    assert len(values) == n_items

    return capacity, weights, values


if __name__ == '__main__':
    capacity, weights, values = load_data('assets/knapsack1.txt.gz')

    t0 = monotonic()
    max_value, ixs = knapsack(capacity, weights, values)
    t1 = monotonic()

    print('Question 1 (small dataset)')
    print(f'value:\t{max_value}')
    print(f'items:\t{ixs}')
    print(f'timing: {t1 - t0:.3f} s')

    capacity, weights, values = load_data('assets/knapsack_big.txt.gz')

    t0 = monotonic()
    max_value = knapsack_max_value(capacity, weights, values)
    t1 = monotonic()

    print('\nQuestion 2 (large dataset), iterative approach')
    print(f'value:\t{max_value}')
    print(f'timing: {t1 - t0:.3f} s')

    t0 = monotonic()
    max_value = knapsack_max_value_recursive(capacity, weights, values)
    t1 = monotonic()

    print('\nQuestion 2 (large dataset), recursive approach')
    print(f'value:\t{max_value}')
    print(f'timing: {t1 - t0:.3f} s')
