import unittest
import time
import os
import pandas as pd
from plot_generator import PlotGenerator

class TestPlotGenerator(unittest.TestCase):

    def setUp(self):
        """Setup method to initialize the PlotGenerator object before each test."""
        self.plot_gen = PlotGenerator()

    def test_plot_creation(self):
        """Test to check if the plot is created successfully."""
        df = pd.DataFrame({
            'Gt_corners': [4, 5, 6],
            'Rb_corners': [3, 5, 7]
        })

        # Call the method to generate the plot
        plot_path = self.plot_gen._plot(df, 'Gt_corners', 'Rb_corners')

        # Check if the plot file is created
        self.assertTrue(os.path.exists(plot_path))
        print(f"Generated plot path: {plot_path}")

    def test_performance(self):
        """Test to check the performance (execution time) of the plot generation."""
        df = pd.DataFrame({
            'Gt_corners': list(range(1000)),
            'Rb_corners': list(range(1000))
        })

        # Measure the time taken to generate the plot
        start_time = time.time()
        self.plot_gen._plot(df, 'Gt_corners', 'Rb_corners')
        execution_time = time.time() - start_time

        # Ensure the execution time is within a reasonable limit (e.g., less than 1 second)
        self.assertLess(execution_time, 1)
        print(f"Execution time: {execution_time:.6f} seconds")

    def test_memory_usage(self):
        """Test to check memory usage during plot generation."""
        import tracemalloc

        tracemalloc.start()

        df = pd.DataFrame({
            'Gt_corners': list(range(1000)),
            'Rb_corners': list(range(1000))
        })

        # Generate the plot and monitor memory usage
        self.plot_gen._plot(df, 'Gt_corners', 'Rb_corners')
        current, peak = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        # Ensure that memory usage does not exceed 10 MB
        self.assertLess(peak / 10**6, 10)
        print(f"Memory usage: current = {current / 10**6:.2f} MB, peak = {peak / 10**6:.2f} MB")

if __name__ == '__main__':
    unittest.main()
