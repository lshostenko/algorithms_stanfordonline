
def _merge(sorted_array_1, sorted_array_2):
    if not sorted_array_1 or not sorted_array_2:
        yield from sorted_array_1
        yield from sorted_array_2
        return

    iter_1 = iter(sorted_array_1)
    iter_2 = iter(sorted_array_2)

    val_1 = next(iter_1)
    val_2 = next(iter_2)

    while True:
        if val_1 > val_2:
            yield val_2

            try:
                val_2 = next(iter_2)
            except StopIteration:
                yield val_1
                break

        else:
            yield val_1
            try:
                val_1 = next(iter_1)

            except StopIteration:
                yield val_2
                break

    yield from iter_1
    yield from iter_2


def mergesort(array):
    length = len(array)

    if length < 2:
        return array

    split_ix = length // 2

    result = _merge(
        mergesort(array[:split_ix]),
        mergesort(array[split_ix:]),
    )

    return list(result)
