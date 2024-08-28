import gzip
from time import monotonic

from scipy.cluster.hierarchy import DisjointSet


def _flip_bit(bits, ix):
    cur_bit = bits[ix]
    bit = '0' if cur_bit == '1' else '1'
    return bits[:ix] + bit + bits[ix + 1:]


def _next_neighbours(point_bits, all_points):
    for i in range(len(point_bits)):
        if point_bits[i] == '1':
            continue

        bits_i = _flip_bit(point_bits, i)
        if bits_i in all_points:
            yield bits_i

        for j in range(i + 1, len(point_bits)):
            bits_ij = _flip_bit(bits_i, j)
            if bits_ij in all_points and bits_ij > point_bits:
                yield bits_ij


def clusterize(points):
    all_points = set(points)
    clusters = DisjointSet(points)

    for p1 in all_points:
        for p2 in _next_neighbours(p1, all_points):
            clusters.merge(p1, p2)

    return clusters


if __name__ == '__main__':
    with gzip.open('assets/clustering_big.txt.gz', mode='rt') as fp:
        num_points = int(fp.readline().split()[0])

        points = sorted(
            ''.join(char for char in line if char.isdigit())
            for line in fp.readlines()
        )

    assert len(points) == num_points

    t0 = monotonic()
    k_max = clusterize(points).n_subsets
    t1 = monotonic()
    print(f'k_max:\t{k_max}\ntiming:\t{t1 - t0:.2f} s')
