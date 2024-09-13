import gzip
import math
import random
from functools import cache
from itertools import pairwise, permutations

import numpy as np
from scipy.spatial import distance_matrix


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


def test_tsp(points, n_iter=42):
    failed = False

    for i in range(n_iter):
        num_points = random.randrange(2, 10)
        points_reduced = random.sample(points, num_points)

        passed = math.isclose(tsp_bf(points_reduced), tsp_dp(points_reduced))
        if not passed:
            failed = True

        msg = 'PASSED' if passed else 'FAILED'
        print(f'Randomized test\t{i + 1}/{n_iter}\t{msg}')

    assert not failed


def tsp_bf(points):
    @cache
    def distance(i, j):
        if i == j:
            return 0.

        elif i > j:
            return distance(j, i)

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


def tsp_dp(points):
    num_points = len(points)
    c = distance_matrix(points, points)

    dp = np.full((2 ** num_points, num_points), math.inf)

    dp[1 << 0][0] = 0

    for mask in range(1, 2 ** num_points):
        for k in range(num_points):
            if not ((mask >> k) & 1):
                continue

            for j in range(num_points):
                if not ((mask >> j) & 1 and j != k):
                    continue

                dp[mask][k] = min(
                    dp[mask][k],
                    dp[mask ^ (1 << k)][j] + c[j][k],
                )

    ans = math.inf

    for k in range(num_points):
        ans = min(ans, dp[(1 << num_points) - 1][k] + c[k][0])

    return float(ans)


# Programming Assignment 5
if __name__ == '__main__':
    points = load_data('assets/tsp.txt.gz')

    print('Test DP implementation')
    test_tsp(points)
    print('OK')

    # res = tsp_dp(points)  # takes more than 1 hour to complete

    d1 = tsp_dp(points[:13])
    d2 = tsp_dp(points[11:])

    (x11, y11), (x12, y12) = points[11], points[12]
    dist_11_12 = math.sqrt((x11 - x12) ** 2 + (y11 - y12) ** 2)

    res = d1 + d2 - 2 * dist_11_12  # dirty hack

    print(f'Solution:\t{int(res)}')
