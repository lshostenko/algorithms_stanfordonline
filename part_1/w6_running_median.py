import gzip
import heapq


class MedianFinder:
    def __init__(self, numbers):
        self.left = []
        self.right = []

        for number in numbers:
            self.add_number(number)

    def _update_median(self):
        if len(self.left) >= len(self.right):
            self.median = - self.left[0]
        else:
            self.median = self.right[0]

    def _rebalance(self):
        if abs(len(self.left) - len(self.right)) > 1:
            if len(self.left) > len(self.right):
                val = - heapq.heappop(self.left)
                heapq.heappush(self.right, val)

            else:
                val = heapq.heappop(self.right)
                heapq.heappush(self.left, - val)

    def add_number(self, number):
        if not self.left or number <= - self.left[0]:
            heapq.heappush(self.left, - number)
        else:
            heapq.heappush(self.right, number)

        self._rebalance()
        self._update_median()

    def get_median(self):
        if hasattr(self, 'median'):
            return self.median


# Programming Assignment 6 - Question 2
if __name__ == '__main__':
    with gzip.open('assets/Median.txt.gz', mode='rt') as fp:
        numbers = [int(i) for i in fp.read().split()]

    DIVISOR = 10000
    median_sum = 0
    median_finder = MedianFinder([])

    for num in numbers:
        median_finder.add_number(num)
        current_median = median_finder.get_median()
        median_sum = (median_sum + current_median) % DIVISOR

    print(median_sum)
