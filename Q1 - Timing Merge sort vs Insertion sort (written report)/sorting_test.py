import unittest
import random
import timeit
from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

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

    def merge_sort(self, arr: List[int]) -> List[int]:
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]

            self.merge_sort(L)
            self.merge_sort(R)

            i = j = k = 0

            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
        return arr

class TestSortingAlgorithms(unittest.TestCase):
    def setUp(self):
        self.sorter = SortingAlgorithms()
        
    def test_basic_sorting(self):
        # Test already sorted array
        sorted_array = [1, 2, 3, 4, 5]
        self.assertEqual(self.sorter.insertion_sort(sorted_array.copy()), sorted_array)
        
        # Test reverse sorted array
        reverse_array = [5, 4, 3, 2, 1]
        self.assertEqual(self.sorter.insertion_sort(reverse_array.copy()), sorted_array)
        
        # Test random array
        random_array = [3, 1, 4, 5, 2]
        self.assertEqual(self.sorter.insertion_sort(random_array.copy()), sorted_array)
        
    def test_performance_comparison(self):
        sizes = [10, 25, 50, 60, 80, 100, 500, 1000]
        insertion_times = []
        merge_times = []
        faster_algorithm = []

        for size in sizes:
            array = random.sample(range(size * 10), size)
            insertion_time = round(timeit.timeit(lambda: self.sorter.insertion_sort(array.copy()), number=10), 10)
            merge_time = round(timeit.timeit(lambda: self.sorter.merge_sort(array.copy()), number=10), 10)
            insertion_times.append(insertion_time)
            merge_times.append(merge_time)
            faster_algorithm.append('Insertion Sort' if insertion_time < merge_time else 'Merge Sort')

            # Generate individual graphs for each size
            plt.figure()
            plt.bar(['Insertion Sort', 'Merge Sort'], [insertion_time, merge_time])
            plt.title(f'Performance for size {size}')
            plt.ylabel('Time (seconds)')
            plt.savefig(f'images/performance_{size}.png')
            plt.close()

        # Generate total time comparison graph
        plt.figure()
        plt.plot(sizes, insertion_times, label='Insertion Sort', marker='o')
        plt.plot(sizes, merge_times, label='Merge Sort', marker='o')
        plt.xlabel('Input Size')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.title('Total Time Comparison')
        plt.savefig('images/total_performance.png')
        plt.close()

        # Create a DataFrame
        df = pd.DataFrame({
            'Input Size': sizes,
            'Insertion Sort Time (s)': insertion_times,
            'Merge Sort Time (s)': merge_times,
            'Faster Algorithm': faster_algorithm
        })

        # Display the DataFrame in table style
        print(tabulate(df, headers='keys', tablefmt='psql'))

        # Save the DataFrame as an image
        fig, ax = plt.subplots(figsize=(12, 4))  # set size frame
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        plt.savefig('images/performance_comparison_table.png')
        plt.close()

    def test_best_worst_cases(self):
        size = 1000
        # Best case - already sorted
        sorted_array = list(range(size))
        best_case_time_insertion = round(timeit.timeit(
            lambda: self.sorter.insertion_sort(sorted_array.copy()),
            number=10
        ), 10)
        best_case_time_merge = round(timeit.timeit(
            lambda: self.sorter.merge_sort(sorted_array.copy()),
            number=10
        ), 10)
        
        # Worst case - reverse sorted
        reverse_array = list(range(size, 0, -1))
        worst_case_time_insertion = round(timeit.timeit(
            lambda: self.sorter.insertion_sort(reverse_array.copy()),
            number=10
        ), 10)
        worst_case_time_merge = round(timeit.timeit(
            lambda: self.sorter.merge_sort(reverse_array.copy()),
            number=10
        ), 10)

        # Generate graph for best and worst case for insertion sort
        plt.figure()
        plt.bar(['Best Case', 'Worst Case'], [best_case_time_insertion, worst_case_time_insertion])
        plt.title('Best vs Worst Case for Insertion Sort')
        plt.ylabel('Time (seconds)')
        plt.savefig('images/best_worst_case_insertion.png')
        plt.close()

        # Generate graph for best and worst case for merge sort
        plt.figure()
        plt.bar(['Best Case', 'Worst Case'], [best_case_time_merge, worst_case_time_merge])
        plt.title('Best vs Worst Case for Merge Sort')
        plt.ylabel('Time (seconds)')
        plt.savefig('images/best_worst_case_merge.png')
        plt.close()

if __name__ == '__main__':
    unittest.main()

# Citations:
# Insertion Sort: https://www.geeksforgeeks.org/insertion-sort/
# Merge Sort: https://www.geeksforgeeks.org/merge-sort/