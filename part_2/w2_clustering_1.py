import gzip

from scipy.cluster.hierarchy import DisjointSet


def clustering_max_spacing(points, distances, k=4):
    if len(points) < k:
        raise ValueError

    clusters = DisjointSet(points)
    sorted_edges = sorted(distances.keys(), key=distances.get)
    sorted_edges = iter(sorted_edges)

    while clusters.n_subsets > k:
        try:
            p1, p2 = next(sorted_edges)
        except StopIteration:
            raise ValueError

        if clusters.connected(p1, p2):
            continue

        clusters.merge(p1, p2)

    for edge in sorted_edges:
        if not clusters.connected(*edge):
            return distances[edge]


if __name__ == '__main__':
    with gzip.open('assets/clustering1.txt.gz', mode='rt') as fp:
        distances = {}
        num_points = int(fp.readline())
        points = set()

        for line in fp.readlines():
            p1, p2, weight = map(int, line.split())
            edge = p1, p2

            distances[edge] = weight
            points.update(edge)

    assert len(points) == num_points

    print(clustering_max_spacing(points, distances, k=4))
