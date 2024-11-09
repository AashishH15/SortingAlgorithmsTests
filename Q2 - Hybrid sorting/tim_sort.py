from typing import List
import random
import timeit
import matplotlib.pyplot as plt
import os

class SortingAlgorithms:
    def insertion_sort(self, arr: List[int]) -> List[int]:
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    def merge_sort(self, arr: List[int], k: int) -> List[int]:
        if len(arr) <= k:
            return self.insertion_sort(arr)
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]

            self.merge_sort(L, k)
            self.merge_sort(R, k)

            i = j = m = 0

            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    arr[m] = L[i]
                    i += 1
                else:
                    arr[m] = R[j]
                    j += 1
                m += 1

            while i < len(L):
                arr[m] = L[i]
                i += 1
                m += 1

            while j < len(R):
                arr[m] = R[j]
                j += 1
                m += 1
        return arr

def experiment():
    sizes = [10, 25, 50, 60, 80, 100, 500, 1000]
    k_values = range(2, 21, 2)
    sorter = SortingAlgorithms()

    output_dir = 'Q2 - Hybrid sorting/images'
    os.makedirs(output_dir, exist_ok=True)

    overall_tim_sort_times = {k: [] for k in k_values}

    for size in sizes:
        insertion_times = []
        merge_times = []
        tim_sort_times = {k: [] for k in k_values}

        for _ in range(5):  # Repeat each experiment 5 times for averaging
            array = random.sample(range(size * 10), size)
            insertion_times.append(timeit.timeit(lambda: sorter.insertion_sort(array.copy()), number=10))
            merge_times.append(timeit.timeit(lambda: sorter.merge_sort(array.copy(), size), number=10))
            for k in k_values:
                tim_sort_times[k].append(timeit.timeit(lambda: sorter.merge_sort(array.copy(), k), number=10))

        avg_insertion_time = sum(insertion_times) / len(insertion_times)
        avg_merge_time = sum(merge_times) / len(merge_times)
        avg_tim_sort_times = {k: sum(times) / len(times) for k, times in tim_sort_times.items()}

        for k in k_values:
            overall_tim_sort_times[k].append(avg_tim_sort_times[k])

        plt.figure()
        plt.plot(k_values, [avg_tim_sort_times[k] for k in k_values], label='Tim Sort')
        plt.axhline(y=avg_insertion_time, color='r', linestyle='-', label='Insertion Sort')
        plt.axhline(y=avg_merge_time, color='b', linestyle='-', label='Merge Sort')
        plt.xlabel('k value')
        plt.ylabel('Time (seconds)')
        plt.title(f'Performance Comparison for size {size}')
        plt.xticks(k_values)  # Set x-axis ticks to full numbers
        plt.legend()
        plt.savefig(os.path.join(output_dir, f'tim_sort_performance_{size}.png'))
        plt.close()

    # Generate the overall optimal k value graph
    avg_overall_tim_sort_times = {k: sum(times) / len(times) for k, times in overall_tim_sort_times.items()}
    plt.figure()
    plt.plot(k_values, [avg_overall_tim_sort_times[k] for k in k_values], label='Tim Sort')
    plt.xlabel('k value')
    plt.ylabel('Average Time (seconds)')
    plt.title('Optimal k Value Determination')
    plt.xticks(k_values)  # Set x-axis ticks to full numbers
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'tim_sort_optimal_k.png'))
    plt.close()

if __name__ == '__main__':
    experiment()
