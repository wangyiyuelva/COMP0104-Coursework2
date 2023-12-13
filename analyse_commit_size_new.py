import pandas as pd
import matplotlib.pyplot as plt
import csv

def aggregate_commit_data(df):
    # Convert string representations of numbers into actual integers
    df['test_commit_files'] = df['test_commit_files'].astype(int)
    df['test_commit_lines'] = df['test_commit_lines'].astype(int)

    # Group by commit hash and aggregate
    grouped = df.groupby('hash_test_creation')
    aggregated_data = grouped.agg({
        'test_commit_files': 'first',  # Taking the first instance
        'test_commit_lines': 'first'   # Taking the first instance
    }).rename(columns={
        'test_commit_files': 'total_files',
        'test_commit_lines': 'total_lines'
    })

    # Calculate total commit size
    aggregated_data['commit_size'] = aggregated_data['total_files'] + aggregated_data['total_lines']
    return aggregated_data

def analyze_same_commit_sizes_standard_deviation(csv_file):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        commit_data = [row for row in reader if row['type'] == 'same']
        
    df = pd.DataFrame(commit_data)
    aggregated_data = aggregate_commit_data(df)

    # Calculate statistical metrics for commit sizes
    mean = aggregated_data['commit_size'].mean()
    std_dev = aggregated_data['commit_size'].std()

    # Ensure that the small_threshold is not negative
    small_threshold = max(mean - std_dev, 0)
    large_threshold = mean + std_dev

    # Categorize commit sizes based on calculated thresholds
    size_categories = pd.cut(aggregated_data['commit_size'], 
                             bins=[-float('inf'), small_threshold, large_threshold, float('inf')], 
                             labels=['small', 'medium', 'large'])

    # Count the number of commits in each size category
    size_counts = size_categories.value_counts().to_dict()

    # Print descriptive statistics
    print(f"Descriptive Statistics for Commit Sizes (Standard Deviation Method):")
    print(f"Mean commit size: {mean}")
    print(f"Standard Deviation of commit size: {std_dev}")
    print(f"Small threshold: {small_threshold}")
    print(f"Large threshold: {large_threshold}")

    # Plot histogram
    plt.hist(aggregated_data['commit_size'], bins=30, alpha=0.5, color='blue', edgecolor='black')
    plt.axvline(mean, color='red', linestyle='dashed', linewidth=2, label='Mean')
    plt.axvline(small_threshold, color='green', linestyle='dashed', linewidth=2, label='Small threshold')
    plt.axvline(large_threshold, color='orange', linestyle='dashed', linewidth=2, label='Large threshold')
    plt.title('Histogram of Commit Sizes (Standard Deviation Method)')
    plt.xlabel('Commit Size')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

    return size_counts

def analyze_same_commit_sizes_percentile(csv_file):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        commit_data = [row for row in reader if row['type'] == 'same']
        
    df = pd.DataFrame(commit_data)
    aggregated_data = aggregate_commit_data(df)

    # Calculate percentiles for commit sizes
    small_threshold = aggregated_data['commit_size'].quantile(0.25)
    medium_threshold = aggregated_data['commit_size'].quantile(0.75)

    # Categorize commit sizes based on quartiles
    size_categories = pd.cut(aggregated_data['commit_size'], 
                             bins=[-float('inf'), small_threshold, medium_threshold, float('inf')], 
                             labels=['small', 'medium', 'large'])

    # Count the number of commits in each size category
    size_counts = size_categories.value_counts().to_dict()

    # Print descriptive statistics
    print(f"Descriptive Statistics for Commit Sizes (Percentile Method):")
    print(f"Mean commit size: {aggregated_data['commit_size'].mean()}")
    print(f"Standard Deviation of commit size: {aggregated_data['commit_size'].std()}")
    print(f"Small threshold (25th percentile): {small_threshold}")
    print(f"Medium threshold (75th percentile): {medium_threshold}")

    # Plot histogram
    plt.hist(aggregated_data['commit_size'], bins=30, alpha=0.5, color='blue', edgecolor='black')
    plt.axvline(aggregated_data['commit_size'].mean(), color='red', linestyle='dashed', linewidth=2, label='Mean')
    plt.axvline(small_threshold, color='green', linestyle='dashed', linewidth=2, label='Small threshold (25th percentile)')
    plt.axvline(medium_threshold, color='orange', linestyle='dashed', linewidth=2, label='Medium threshold (75th percentile)')
    plt.title('Histogram of Commit Sizes (Percentile Method)')
    plt.xlabel('Commit Size')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

    return size_counts

csv_file = './analyseTestfile/analyse_iceberg.csv'  # Replace with the path to CSV file

# size_counts_sd = analyze_same_commit_sizes_standard_deviation(csv_file)
size_counts_percentile = analyze_same_commit_sizes_percentile(csv_file)

# print(f"Commit Size Counts (Standard Deviation Method): {size_counts_sd}")
print(f"Commit Size Counts (Percentile Method): {size_counts_percentile}")



