import numpy as np


def _calculate_table(capacity, weights, values):
    _check_args(capacity, weights, values)

    dtype = np.min_scalar_type(sum(values))
    num_items = len(values)
    weights, values = np.array(weights), np.array(values)

    table = np.empty((num_items + 1, capacity + 1), dtype=dtype)
    table[0, :] = 0
    table[:, 0] = 0

    for i in range(1, num_items + 1):
        mask_keep = np.hstack((
            [True],
            np.arange(1, capacity + 1) < weights[i - 1]
        ))
        mask_update = np.invert(mask_keep)
        ixs_update = np.arange(capacity + 1)[mask_update] - weights[i - 1]

        table[i, mask_keep] = table[i - 1, mask_keep]
        table[i, mask_update] = np.maximum(
            table[i - 1, mask_update],
            table[i - 1, ixs_update] + values[i - 1],
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
