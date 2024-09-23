import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns


class PlotGenerator:
    def __init__(self, output_folder="plots"):
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def draw_plots(self, json_file):
        # Load data from json
        df = pd.read_json(json_file)

        df['corner_category'] = pd.cut(df['gt_corners'], bins=[0, 4, 8, float('inf')],
                                       labels=['Small rooms', 'Medium rooms', 'Large rooms'])

        # Create various plots
        plots = {}
        plots['corner_comparison'] = self.plot_gt_vs_rb_corners(df)
        plots['deviation_analysis'] = self.plot_error_bars(df)
        plots['floor_vs_ceiling'] = self.plot_floor_vs_ceiling(df)
        plots['deviation_boxplot'] = self.plot_deviation_boxplot(df)
        plots['deviation_trends'] = self.plot_deviation_trends(df)
        plots['scatter_corners_vs_deviation'] = self.plot_scatter_corners_vs_deviation(df)

        return plots

    def save_and_close_plot(self, plot_name):
        plot_path = os.path.join(self.output_folder, plot_name)
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
        return plot_path

    def plot_gt_vs_rb_corners(self, df):
        plt.figure(figsize=(10, 6))
        df.groupby('corner_category', observed=True)[['gt_corners', 'rb_corners']].mean().plot(kind='bar')
        plt.title('Ground Truth vs Predicted Corners by Room Category')
        plt.ylabel('Average Number of Corners')
        plt.xlabel('Room Category')
        plt.legend(['Ground Truth', 'Predicted'])
        return self.save_and_close_plot('grouped_gt_vs_rb_corners.png')

    def plot_error_bars(self, df):
        plt.figure(figsize=(10, 6))

        grouped_df = df.groupby('corner_category', observed=True).agg({
            'mean': ['mean', 'min', 'max']
        })

        grouped_df.columns = ['_'.join(col).strip() for col in grouped_df.columns.values]

        plt.errorbar(grouped_df.index, grouped_df['mean_mean'],
                     yerr=[grouped_df['mean_mean'] - grouped_df['mean_min'],
                           grouped_df['mean_max'] - grouped_df['mean_mean']],
                     fmt='o', capsize=5, capthick=2, ecolor='red', markersize=8)

        plt.title('Mean Deviation with Min/Max Error Bars by Room Category')
        plt.ylabel('Deviation in Degrees')
        plt.xlabel('Room Category')
        plt.grid(True, linestyle='--', alpha=0.7)

        return self.save_and_close_plot('grouped_mean_deviation_error_bars.png')

    def plot_floor_vs_ceiling(self, df):
        plt.figure(figsize=(10, 6))
        df.groupby('corner_category', observed=True)[['floor_mean', 'ceiling_mean']].mean().plot(kind='bar', stacked=True)
        plt.title('Floor vs Ceiling Mean Deviations by Room Category')
        plt.ylabel('Mean Deviation in Degrees')
        plt.xlabel('Room Category')
        plt.legend(['Floor', 'Ceiling'])
        return self.save_and_close_plot('grouped_floor_vs_ceiling.png')

    def plot_deviation_boxplot(self, df):
        plt.figure(figsize=(12, 6))
        deviation_data = pd.melt(df[['floor_max', 'ceiling_max', 'floor_min', 'ceiling_min']],
                                 var_name='Type', value_name='Deviation')
        sns.boxplot(x='Type', y='Deviation', data=deviation_data)
        plt.title('Distribution of Floor and Ceiling Deviations')
        plt.ylabel('Deviation in Degrees')
        plt.xlabel('Deviation Type')
        plt.xticks(rotation=45)
        return self.save_and_close_plot('deviation_boxplot.png')

    def plot_deviation_trends(self, df):
        plt.figure(figsize=(10, 6))

        grouped_df = df.groupby('corner_category', observed=True).agg({
            'floor_mean': 'mean',
            'ceiling_mean': 'mean'
        })

        plt.plot(grouped_df.index, grouped_df['floor_mean'],
                 label='Floor Mean Deviation', marker='o', linewidth=2)
        plt.plot(grouped_df.index, grouped_df['ceiling_mean'],
                 label='Ceiling Mean Deviation', marker='s', linewidth=2)

        plt.title('Corner-wise Deviation Trends by Room Category')
        plt.ylabel('Mean Deviation in Degrees')
        plt.xlabel('Room Category')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)

        return self.save_and_close_plot('grouped_deviation_trends.png')

    def plot_scatter_corners_vs_deviation(self, df):
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(df['gt_corners'], df['rb_corners'], c=df['mean'], cmap='coolwarm', s=100, alpha=0.7)
        plt.title('Predicted vs Actual Corners (Color-coded by Mean Deviation)')
        plt.xlabel('Ground Truth Corners')
        plt.ylabel('Predicted Corners')
        plt.colorbar(scatter, label='Mean Deviation (Degrees)')
        plt.grid(True, linestyle='--', alpha=0.5)
        return self.save_and_close_plot('scatter_corners_vs_deviation.png')


if __name__ == '__main__':
    plot = PlotGenerator()
    plot.draw_plots('data/deviations.json')
