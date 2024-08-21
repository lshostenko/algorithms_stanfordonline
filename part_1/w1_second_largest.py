
def second_largest(array):
    '''
    Assumes all values in 'array' are distinct
    '''
    if len(array) == 2:
        return min(array)

    elif len(array) < 2:
        raise ValueError('At least two elements are required.')

    reduced_array = [
        max(array[2 * i: 2 * i + 2]) for i in range(len(array) // 2)
    ]
    if len(array) % 2:
        reduced_array.append(array[-1])

    return second_largest(reduced_array)
