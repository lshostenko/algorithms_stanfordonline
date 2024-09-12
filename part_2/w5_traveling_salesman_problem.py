import gzip
import math
from functools import cache
from itertools import pairwise, permutations


def load_data(filename):
    if filename.endswith('.gz'):
        open_file = gzip.open
    else:
        open_file = open

    data = []

    with open_file(filename, mode='rt') as fp:
        num_cities = int(fp.readline().strip())

        for line in fp.readlines():
            x, y = map(float, line.split())
            data.append((x, y))

    assert len(data) == num_cities

    return data


def tsp_bf(points):
    @cache
    def distance(i, j):
        x_i, y_i = points[i]
        x_j, y_j = points[j]
        return math.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)

    min_distance = math.inf

    for ixs in permutations(range(len(points))):
        cur_distance = sum(distance(i, j) for i, j in pairwise(ixs))
        cur_distance += distance(ixs[0], ixs[-1])

        if cur_distance < min_distance:
            min_distance = cur_distance

    return min_distance


if __name__ == '__main__':
    points = load_data('assets/tsp.txt.gz')
    res = tsp_bf(points[:10])

    print(res)
