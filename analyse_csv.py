import csv
import sys
import ast
from datetime import datetime

# Increase the maximum field size limit
csv.field_size_limit(sys.maxsize)

# Function to determine if a filename represents a test file
def is_test_file(filename):
    return filename.startswith('Test') or filename.endswith('Test.java')

# Function to get the corresponding implementation file name from a test file name
def get_impl_filename(test_filename):
    if test_filename.startswith('Test'):
        return test_filename[4:]  # Remove the prefix 'Test' for matching
    if test_filename.endswith('Test.java'):
        return test_filename.replace('Test.java', '.java')  # Replace 'Test.java' with '.java' for matching
    return None

# Function to process the CSV and analyze the data
def analyze_test_file_creation(csv_path):
    # Dictionary to store the creation times of files
    file_creation_times = {}

    # Read the CSV file
    with open(csv_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parse the committer date
            commit_date = datetime.strptime(row['committer_date'], '%Y-%m-%d %H:%M:%S%z')
            # Safely evaluate the string representation of a list into an actual list
            modified_files = ast.literal_eval(row['modified_file'])

            # Record the creation date for all files
            for filename in modified_files:
                # Assume that the file is new if not present in the dictionary
                if filename not in file_creation_times:
                    file_creation_times[filename] = commit_date

    # Initialize counters for before, after, and same commit
    before_count = after_count = same_commit_count = 0

    # Analyze the creation times by comparing test files with their corresponding implementation files
    for filename, commit_date in file_creation_times.items():
        if is_test_file(filename):
            impl_filename = get_impl_filename(filename)
            if impl_filename and impl_filename in file_creation_times:
                impl_commit_date = file_creation_times[impl_filename]
                if commit_date < impl_commit_date:
                    before_count += 1
                elif commit_date > impl_commit_date:
                    after_count += 1
                else:
                    same_commit_count += 1

    return before_count, after_count, same_commit_count

# Path to the CSV file - replace with the correct path
csv_file_path = 'pydrillerData/my.csv'

# Perform the analysis
before, after, same_commit = analyze_test_file_creation(csv_file_path)

# Output the results
print(f"Test files created before implementation files: {before}")
print(f"Test files created after implementation files: {after}")
print(f"Test files created in the same commit as implementation files: {same_commit}")
