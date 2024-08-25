import gzip
from copy import copy


def calculate_total_cost(scheduled_jobs):
    cost = 0
    completion_time = 0

    for weight, lenght in scheduled_jobs:
        completion_time += lenght
        cost += weight * completion_time

    return cost


# Programming Assignment 1 - Questions 1 & 2
if __name__ == '__main__':
    with gzip.open('assets/jobs.txt.gz', mode='rt') as fp:
        jobs = []
        num_jobs = int(fp.readline())

        for line in fp.readlines():
            w, j = line.split()
            jobs.append((int(w), int(j)))

        assert len(jobs) == num_jobs

    jobs_1 = copy(jobs)
    jobs_1.sort(reverse=True)
    jobs_1.sort(key=lambda x: x[0] - x[1], reverse=True)
    res_1 = calculate_total_cost(jobs_1)

    jobs_2 = copy(jobs)
    jobs_2.sort(key=lambda x: x[0] / x[1], reverse=True)
    res_2 = calculate_total_cost(jobs_2)

    print(f'total cost, jobs ordered by (weight - lenght):\t{res_1}')
    print(f'total cost, jobs ordered by (weight / lenght):\t{res_2}')
