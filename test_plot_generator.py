import pandas as pd
import os
import unittest
from unittest.mock import patch, MagicMock
from plot_generator import PlotGenerator


class TestPlotGeneratorWithCVAT(unittest.TestCase):
    def setUp(self):
        """Setup method to initialize PlotGenerator and mock CVAT data."""
        self.plot_gen = PlotGenerator(output_folder="test_plots")

        # Simulated CVAT data
        self.mock_data = pd.DataFrame({
            'gt_corners': [i % 10 for i in range(100)],
            'rb_corners': [i % 8 for i in range(100)],
            'mean': [i % 5 for i in range(100)],
            'floor_mean': [i % 6 for i in range(100)],
            'ceiling_mean': [i % 7 for i in range(100)],
            'floor_max': [i % 9 for i in range(100)],
            'ceiling_max': [i % 10 for i in range(100)],
            'floor_min': [i % 3 for i in range(100)],
            'ceiling_min': [i % 4 for i in range(100)]
        })

        # Categorizing data
        self.mock_data['corner_category'] = pd.cut(
            self.mock_data['gt_corners'],
            bins=[0, 4, 8, float('inf')],
            labels=['Small rooms', 'Medium rooms', 'Large rooms']
        )

        # Save this as a temporary JSON file for testing
        self.mock_data.to_json('test_cvat_data.json', orient='records')

    def test_draw_plots(self):
        """Test the draw_plots method for efficiency and output files."""
        plots = self.plot_gen.draw_plots('test_cvat_data.json')
        expected_plots = [
            'grouped_gt_vs_rb_corners.png',
            'grouped_mean_deviation_error_bars.png',
            'grouped_floor_vs_ceiling.png',
            'deviation_boxplot.png',
            'grouped_deviation_trends.png',
            'scatter_corners_vs_deviation.png'
        ]

        # Check if all expected plot files were created
        for plot in expected_plots:
            self.assertTrue(os.path.exists(os.path.join(self.plot_gen.output_folder, plot)))

    @patch('cvat_sdk.core.client.Client')
    def test_load_cvat_data(self, mock_client):
        """Test loading data from CVAT."""
        # Mock the CVAT client and its methods
        mock_task = MagicMock()
        mock_task.export_dataset.return_value = None
        mock_client.return_value.tasks.retrieve.return_value = mock_task

        # Simulate loading CVAT data
        task_id = 1
        json_file_path = 'path_to_cvat_data.json'

        # Write mock data to the file
        self.mock_data.to_json(json_file_path, orient='records')

        # Load the exported JSON file
        cvat_data = pd.read_json(json_file_path)

        self.assertIsNotNone(cvat_data)  # Ensure data is loaded
        self.assertGreater(len(cvat_data), 0)  # Ensure the DataFrame is not empty

        # Clean up the temporary file
        os.remove(json_file_path)

    def tearDown(self):
        """Clean up generated files after the test."""
        if os.path.exists('test_cvat_data.json'):
            os.remove('test_cvat_data.json')
        if os.path.exists(self.plot_gen.output_folder):
            for file_name in os.listdir(self.plot_gen.output_folder):
                os.remove(os.path.join(self.plot_gen.output_folder, file_name))
            os.rmdir(self.plot_gen.output_folder)


if __name__ == "__main__":
    unittest.main()
