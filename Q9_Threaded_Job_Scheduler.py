"""Q9: Deterministic multi-worker scheduler simulation.

Jobs are selected by higher priority, then earlier arrival. The assignment does
not define a total shared-resource capacity, so worker availability is the
scheduling constraint and the resources field is retained as input metadata.
"""
import heapq
import sys


def main():
    try:
        w, n = map(int, sys.stdin.readline().split())
        if not 1 <= w <= 64 or n < 1:
            raise ValueError
        jobs = []
        for sequence in range(n):
            arrival, job_id, priority, duration, resources = sys.stdin.readline().split()
            job = (int(arrival), job_id, int(priority), int(duration), int(resources), sequence)
            if job[0] < 0 or job[2] < 0 or job[3] < 1 or job[4] < 1:
                raise ValueError
            jobs.append(job)
    except ValueError:
        print("Invalid input.")
        return

    jobs.sort(key=lambda job: (job[0], job[5]))
    workers = [(0, number) for number in range(1, w + 1)]
    heapq.heapify(workers)
    waiting = []
    next_job = 0
    results = []
    waiting_total = 0
    current_time = 0

    while len(results) < n:
        next_arrival = jobs[next_job][0] if next_job < n else float("inf")
        next_free = workers[0][0]

        # Move to the next event without changing any worker's actual free time.
        if not waiting and next_arrival > current_time and next_free <= current_time:
            current_time = next_arrival
        else:
            current_time = max(current_time, min(next_arrival, next_free))

        while next_job < n and jobs[next_job][0] <= current_time:
            arrival, job_id, priority, duration, resources, sequence = jobs[next_job]
            heapq.heappush(waiting, (-priority, arrival, sequence, job_id, duration, resources))
            next_job += 1

        # If a worker is not yet free, the next loop advances to its finish event.
        if not waiting:
            continue

        available_time, worker_id = heapq.heappop(workers)
        if available_time > current_time:
            current_time = available_time
            # Include jobs that arrived while this worker was busy.
            while next_job < n and jobs[next_job][0] <= current_time:
                arrival, job_id, priority, duration, resources, sequence = jobs[next_job]
                heapq.heappush(waiting, (-priority, arrival, sequence, job_id, duration, resources))
                next_job += 1

        neg_priority, arrival, sequence, job_id, duration, resources = heapq.heappop(waiting)
        start_time = max(available_time, arrival, current_time if available_time > current_time else available_time)
        finish_time = start_time + duration
        waiting_total += start_time - arrival
        results.append((sequence, job_id, worker_id, start_time, finish_time))
        heapq.heappush(workers, (finish_time, worker_id))

    for _, job_id, worker_id, start, finish in sorted(results):
        print(job_id, f"W{worker_id}", start, finish)
    print(f"AVG_WAIT {waiting_total / n:.2f}")


if __name__ == "__main__":
    main()
