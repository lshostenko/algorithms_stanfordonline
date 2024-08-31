import numpy as np


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

        table[i, :w_i] = table[i - 1, :w_i]
        table[i, w_i:] = np.maximum(
            table[i - 1, w_i:],
            table[i - 1, :capacity - w_i + 1] + v_i,
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
