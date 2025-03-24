import csv
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

def benchmark_input(row):
    return (row[1], row[2])


def format_time(x, pos):
    if x >= 1_000_000:
        return f' {x / 1_000_000:.1f}ms '
    else:
        return f' {int(x / 1_000):.0f}µs '


if __name__ == "__main__":
    mpl.rcParams['axes.edgecolor'] = '#676466'
    mpl.rcParams['axes.facecolor'] = '#f5f4f3'
    mpl.rcParams['axes.prop_cycle'] = "cycler('color', ['#6768ab'])"
    mpl.rcParams['figure.autolayout'] = True
    mpl.rcParams['figure.titlesize'] = 16
    mpl.rcParams['font.family'] = 'monospace'
    mpl.rcParams['font.size'] = 9
    mpl.rcParams['text.color'] = '#2d282e'
    mpl.rcParams['ytick.labelcolor'] = '#2d282e'
    mpl.rcParams['ytick.labelsize'] = 10
    mpl.rcParams['ytick.color'] = '#676466'

    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)

    with open('benchmark.txt') as file:
        reader = csv.reader(file)
        table = [[row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5])] for row in reader]
        table.sort(key=benchmark_input)
        for key, group in groupby(table, benchmark_input):
            group = list(group)
            group.sort(key=lambda row: row[0])

            labels = [row[0] for row in group]
            values = [row[4] for row in group]  # Using median values (index 4)
            formatted_values = [format_time(value, 0) for value in values]
            sorted_values = sorted(values)
            
            # Adjust margin based on actual data
            margin = sorted_values[-1] * 0.05 if sorted_values else 0

            fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12, 4))
            fig.subplots_adjust(wspace=0.05)
            fig.suptitle(f'Benchmark (pool={key[0]}, workers={key[1]})')
            bar1 = ax1.barh(labels, values)
            bar2 = ax2.barh(labels, values)
            label1 = ax1.bar_label(bar1, labels=formatted_values, color='white')
            label2 = ax2.bar_label(bar2, labels=formatted_values)

            for label in label1:
                label.set_horizontalalignment('right')

            # Handle case with few values
            if len(sorted_values) >= 1:
                min_val = sorted_values[0]
                max_val = sorted_values[-1]
                
                # Set limits appropriately
                ax1.set_xlim(0, min_val * 2)  # Show full range for shortest bar
                if len(sorted_values) > 1:
                    ax2.set_xlim(min_val - margin, max_val + margin)  # Zoom in on differences
                else:
                    ax2.set_xlim(max_val * 0.9, max_val * 1.1)  # Default case
                    
            ax1.spines.right.set_visible(False)
            ax2.spines.left.set_visible(False)
            ax1.xaxis.set_major_formatter(format_time)
            ax2.xaxis.set_major_formatter(format_time)
            ax1.xaxis.set_visible(False)
            ax2.xaxis.set_visible(False)
            ax2.yaxis.set_ticks_position('none')

            fig.savefig(f'results/benchmark_p{key[0]:02}_w{key[1]:03}.svg')
            plt.close(fig)