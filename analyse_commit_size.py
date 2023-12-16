import pandas as pd
import ast
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

# # Function to load data from CSV
# def load_data(csv_file):
#     return pd.read_csv(csv_file)

# Function to count the number of test files in a commit
def count_test_files(modified_files_str):
    try:
        modified_files = ast.literal_eval(modified_files_str)
    except ValueError:
        return 0  # Return 0 if parsing fails
    count = 0
    for file_info in modified_files:
        filename = file_info[0]
        if 'Test' in filename or filename.endswith('Test.java'):
            count += 1
    return count


def prepare_csv(csv_file):
    """
    Bsed one repo information csv file generate lines, files, and commitsize csv file
    TODO: The calculation method of commit size should be furtehr improve
    :param csv_file: the path to the informative csv file
    :return: result_df only contains the hash, the files, the lines and calculated commit size.
    """
    df = pd.read_csv(csv_file)

    # Count the number of test files in each commit
    df['num_test_files'] = df['modified_file'].apply(count_test_files)

    # Convert 'files' and 'lines' columns to numeric
    df['files'] = pd.to_numeric(df['files'], errors='coerce')
    df['lines'] = pd.to_numeric(df['lines'], errors='coerce')

    # Calculate commit size
    df['commit_size'] = df['files'] + df['lines']

    result_df = df[['hash', 'lines', 'files', 'num_test_files', 'commit_size']]
    # Save the new DataFrame to a new CSV file
    result_csv_file = f'./analyseCommitSize/{repo_name}-table_commit_size.csv'  # Replace with desired output CSV file path
    result_df.to_csv(result_csv_file, index=False)

    return result_df


repo_name = 'knox'

# Load data
csv_file = f'./pydrillerData/{repo_name}.csv'  # Replace with your CSV file path

# Create a new DataFrame with required columns
result_df = prepare_csv(csv_file)

# Correlation analysis
correlation, _ = pearsonr(result_df['commit_size'], result_df['num_test_files'])
print(f'Pearson Correlation: {correlation}')

plt.scatter(result_df['commit_size'], result_df['num_test_files'], alpha=0.5)
plt.xlabel('Commit Size')
plt.ylabel('Number of Test files')
plt.title(f'{repo_name} - Correlation between Commit Size and Inclusion of Test Files')
plt.show()
