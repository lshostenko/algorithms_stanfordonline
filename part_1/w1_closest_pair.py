import math
import operator
import random
import time


def euclidean_distance(point_1, point_2):
    d_sqr = (point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2
    return math.sqrt(d_sqr)


def closest_pair_bf(points):
    closest_pair = None, None
    min_distance = math.inf

    for i in range(len(points) - 1):
        p_1 = points[i]

        for p_2 in points[i + 1:]:
            d = euclidean_distance(p_1, p_2)

            if d < min_distance:
                closest_pair = p_1, p_2
                min_distance = d

    return min_distance, closest_pair


def _closest_pair(p_x, p_y):
    if len(p_x) < 4:
        return closest_pair_bf(p_x)

    median_ix = len(p_x) // 2

    left_x, right_x = p_x[:median_ix], p_x[median_ix:]
    x_median = right_x[0][0]

    left_y, right_y = [], []

    for point in p_y:
        if point[0] > x_median:
            right_y.append(point)
        else:
            left_y.append(point)

    delta, best_nonsplit_pair = min(
        _closest_pair(left_x, left_y),
        _closest_pair(right_x, right_y),
    )

    s_y = [p for p in p_y if abs(p[0] - x_median) < delta]
    best_split_distance = delta
    best_split_pair = None

    for i, point_1 in enumerate(s_y[:-1]):
        for point_2 in s_y[i + 1: i + 8]:
            if point_2[1] - point_1[1] > best_split_distance:
                break
            else:
                distance = euclidean_distance(point_1, point_2)
                if distance < best_split_distance:
                    best_split_distance = distance
                    best_split_pair = point_1, point_2

    if best_split_pair is not None:
        return best_split_distance, best_split_pair

    return delta, best_nonsplit_pair


def closest_pair(points):
    p_x = sorted(points, key=operator.itemgetter(0))
    p_y = sorted(points, key=operator.itemgetter(1))

    return _closest_pair(p_x, p_y)


# points = [
#     (1000 * random.random(), 1000 * random.random())
#     for i in range(10000)
# ]

# t0 = time.monotonic()
# d1, pair1 = closest_pair_bf(points)
# t1 = time.monotonic()

# d2, pair2 = closest_pair(points)
# t2 = time.monotonic()

# assert math.isclose(d1, d2)
# assert sorted(pair1) == sorted(pair2)

# print('timing for brute force algorithm:', t1 - t0)
# print('timing for divide and conquer algorithm:', t2 - t1)

# for i in range(100):
#     points = [
#         (100 * random.random(), 100 * random.random())
#         for i in range(1000)
#     ]

#     d1, pair1 = closest_pair_bf(points)
#     d2, pair2 = closest_pair(points)

#     assert math.isclose(d1, d2)
#     assert sorted(pair1) == sorted(pair2)
