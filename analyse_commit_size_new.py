import pandas as pd
import matplotlib.pyplot as plt
import csv

def analyze_same_commit_sizes_standard_deviation(csv_file):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        commit_data = [row for row in reader if row['type'] == 'same']
        
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(commit_data)

    # Convert string representations of numbers into actual integers
    df['test_commit_files'] = df['test_commit_files'].astype(int)
    df['test_commit_lines'] = df['test_commit_lines'].astype(int)

    # Calculate commit sizes as the sum of files and lines
    df['commit_size'] = df['test_commit_files'] + df['test_commit_lines']
    
    # Calculate statistical metrics for commit sizes
    mean = df['commit_size'].mean()
    std_dev = df['commit_size'].std()
    min_size = df['commit_size'].min()
    max_size = df['commit_size'].max()

    # Ensure that the small_threshold is not negative
    small_threshold = max(mean - std_dev, 0)
    large_threshold = mean + std_dev

    # Categorize commit sizes based on calculated thresholds
    size_categories = pd.cut(df['commit_size'], 
                             bins=[-float('inf'), small_threshold, large_threshold, float('inf')], 
                             labels=['small', 'medium', 'large'])

    # Count the number of commits in each size category
    size_counts = size_categories.value_counts().to_dict()

    # Print descriptive statistics
    print(f"Descriptive Statistics for Commit Sizes:")
    print(f"Mean commit size: {mean}")
    print(f"Standard Deviation of commit size: {std_dev}")
    print(f"Minimum commit size: {min_size}")
    print(f"Maximum commit size: {max_size}")
    print(f"Small threshold: {small_threshold}")
    print(f"Large threshold: {large_threshold}")

    # Plot histogram
    plt.hist(df['commit_size'], bins=30, alpha=0.5, color='blue', edgecolor='black')
    plt.axvline(mean, color='red', linestyle='dashed', linewidth=2, label='Mean')
    plt.axvline(small_threshold, color='green', linestyle='dashed', linewidth=2, label='Small threshold')
    plt.axvline(large_threshold, color='orange', linestyle='dashed', linewidth=2, label='Large threshold')
    plt.title('Histogram of Commit Sizes')
    plt.xlabel('Commit Size')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

    return size_counts

def analyze_same_commit_sizes_percentile(csv_file):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        commit_data = [row for row in reader if row['type'] == 'same']
        
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(commit_data)

    # Convert string representations of numbers into actual integers
    df['test_commit_files'] = df['test_commit_files'].astype(int)
    df['test_commit_lines'] = df['test_commit_lines'].astype(int)

    # Calculate commit sizes as the sum of files and lines
    df['commit_size'] = df['test_commit_files'] + df['test_commit_lines']
    
    # Calculate percentiles for commit sizes
    small_threshold = df['commit_size'].quantile(0.25)
    medium_threshold = df['commit_size'].quantile(0.75)
    large_threshold = df['commit_size'].quantile(0.95)  # 95th percentile for large commits

    # Categorize commit sizes based on quartiles and the 95th percentile
    bins = [-float('inf'), small_threshold, medium_threshold, large_threshold, float('inf')]
    labels = ['small', 'medium', 'large', 'very large']
    size_categories = pd.cut(df['commit_size'], bins=bins, labels=labels)

    # Count the number of commits in each size category
    size_counts = size_categories.value_counts().to_dict()

    # Print statistics
    print(f"Descriptive Statistics for Commit Sizes:")
    print(f"Mean commit size: {df['commit_size'].mean()}")
    print(f"Standard Deviation of commit size: {df['commit_size'].std()}")
    print(f"Minimum commit size: {df['commit_size'].min()}")
    print(f"Maximum commit size: {df['commit_size'].max()}")
    print(f"Small threshold (25th percentile): {small_threshold}")
    print(f"Medium threshold (75th percentile): {medium_threshold}")
    print(f"Large threshold (95th percentile): {large_threshold}")

    # Plot histogram
    plt.hist(df['commit_size'], bins=30, alpha=0.5, color='blue', edgecolor='black')
    plt.axvline(df['commit_size'].mean(), color='red', linestyle='dashed', linewidth=2, label='Mean')
    plt.axvline(small_threshold, color='green', linestyle='dashed', linewidth=2, label='Small threshold (25th percentile)')
    plt.axvline(medium_threshold, color='orange', linestyle='dashed', linewidth=2, label='Medium threshold (75th percentile)')
    plt.axvline(large_threshold, color='purple', linestyle='dashed', linewidth=2, label='Large threshold (95th percentile)')
    plt.title('Histogram of Commit Sizes')
    plt.xlabel('Commit Size')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

    return size_counts

csv_file = './analyseTestfile/analyse_iceberg.csv'  # Replace with the path to your CSV file
size_counts = analyze_same_commit_sizes_percentile(csv_file)
# size_counts = analyze_same_commit_sizes_standard_deviation(csv_file)
print(f"Commit Size Counts: {size_counts}")


