import gzip
import multiprocessing as mp
import time


def two_sum_single(target, all_values):
    for v1 in all_values:
        v2 = target - v1

        if v2 in all_values and v2 != v1:
            return 1

    return 0


def two_sum_multiple(targets, all_values):
    return sum(two_sum_single(t, all_values) for t in targets)


def batched_range(i_min, i_max, step, num_split):
    full_range = range(i_min, i_max, step)
    k, m = divmod(len(full_range), num_split)

    for i in range(num_split):
        yield full_range[i * k + min(i, m): (i + 1) * k + min(i + 1, m)]


# Programming Assignment 6 - Question 1
if __name__ == '__main__':
    filename = 'assets/algo1-programming_prob-2sum.txt.gz'
    with gzip.open(filename, mode='rt') as fp:
        all_values = {int(i) for i in fp.readlines()}

    t0 = time.monotonic()

    num_processes = max(mp.cpu_count() - 1, 2)

    def f(targets):
        return two_sum_multiple(targets, all_values)

    with mp.Pool(num_processes) as p:
        result = p.map(f, batched_range(-10000, 10001, 1, 200))

    t1 = time.monotonic()

    print(f'result: {sum(result)}\ttiming: {t1 - t0:.2f} s')
