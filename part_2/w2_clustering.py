import gzip

if __name__ == '__main__':
    with gzip.open('assets/clustering1.txt.gz', mode='rt') as fp:
        edges = []
        num_vertices = int(fp.readline())
        vertices = set()

        for line in fp.readlines():
            v1, v2, weight = map(int, line.split())
            edges.append((v1, v2, weight))
            vertices.update((v1, v2))

        assert len(vertices) == num_vertices
