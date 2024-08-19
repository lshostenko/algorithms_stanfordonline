
def _merge(sorted_array_1, sorted_array_2):
    if not sorted_array_1 or not sorted_array_2:
        return 0, sorted_array_1 + sorted_array_2

    merged_array = []
    inversions = 0

    iter_1 = iter(sorted_array_1)
    iter_2 = iter(sorted_array_2)
    inv_count = len(sorted_array_1)

    val_1 = next(iter_1)
    val_2 = next(iter_2)

    while True:
        if val_1 > val_2:
            merged_array.append(val_2)
            inversions += inv_count

            try:
                val_2 = next(iter_2)
            except StopIteration:
                merged_array.append(val_1)
                break

        else:
            merged_array.append(val_1)
            try:
                val_1 = next(iter_1)
                inv_count -= 1

            except StopIteration:
                merged_array.append(val_2)
                break

    merged_array.extend(iter_1)
    merged_array.extend(iter_2)

    return inversions, merged_array


def count_inversions(array):
    length = len(array)

    if length < 2:
        return 0, array

    split_ix = length // 2

    count_1, array_1 = count_inversions(array[:split_ix])
    count_2, array_2 = count_inversions(array[split_ix:])

    count_m, merged_array = _merge(array_1, array_2)

    return count_1 + count_2 + count_m, merged_array


# Programming Assignment 1
if __name__ == '__main__':
    with open('assets/IntegerArray.txt', mode='rt') as fp:
        array = [int(i) for i in fp.read().split()]

    count, _ = count_inversions(array)
    print(count)
