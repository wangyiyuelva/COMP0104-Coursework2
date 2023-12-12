import csv
import sys
import ast
from datetime import datetime

# Increase the maximum field size limit
# csv.field_size_limit(sys.maxsize)
csv.field_size_limit(131072 * 10)

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
def analyze_test_file_creation(csv_file):
    # Dictionary to store the creation times of files
    file_creation_times = {}
    # Dictionary to store the hash with corresponding creation time
    file_time_hash = {}
    # Dictionary to store the hash with corresponding changed files and LOC
    file_commit_size = {}

    # Read the CSV file
    with open('./pydrillerData/' + csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parse the committer date
            commit_date = datetime.strptime(row['committer_date'], '%Y-%m-%d %H:%M:%S%z')
            # Safely evaluate the string representation of a list into an actual list
            modified_files = ast.literal_eval(row['modified_file'])

            # Record the creation date for all files
            for filename in modified_files:
                if filename[0] not in file_creation_times:
                    if filename[1] == 'ADD':
                        file_creation_times[filename[0]] = commit_date
                        file_time_hash[commit_date] = row['hash']
                        file_commit_size[row['hash']] = [int(row['files']), int(row['lines'])]
                # # Assume that the file is new if not present in the dictionary
                # if filename[0] not in file_creation_times:
                #     file_creation_times[filename[0]] = commit_date
                #     file_time_hash[commit_date] = row['hash']

    new_file_path = './analyseTestfile/analyse_' + csv_file
    with open(new_file_path, 'w', newline='') as file:
        fields = ['type',
                  'test_file', 'hash_test_creation', 'test_creation_time', 'test_commit_files', 'test_commit_lines',
                  'impl_file', 'hash_impl_creation', 'impl_creation_time', 'impl_commit_files', 'impl_commit_lines']
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writerow({'type': 'type', 'test_file': 'test_file', 'hash_test_creation': 'hash_test_creation',
                         'test_creation_time': 'test_creation_time', 'test_commit_files': 'test_commit_files',
                         'test_commit_lines': 'test_commit_lines', 'impl_file': 'impl_file',
                         'hash_impl_creation': 'hash_impl_creation',  'impl_creation_time': 'impl_creation_time',
                         'impl_commit_files': 'impl_commit_files', 'impl_commit_lines': 'impl_commit_lines'})

        # Initialize counters for before, after, and same commit
        before_count = after_count = same_commit_count = 0

        # Analyze the creation times by comparing test files with their corresponding implementation files
        for filename, commit_date in file_creation_times.items():
            if is_test_file(filename):
                test_filename = filename
                impl_filename = get_impl_filename(filename)
                if test_filename and impl_filename in file_creation_times:
                    impl_commit_date = file_creation_times[impl_filename]
                    if commit_date < impl_commit_date:
                        before_count += 1
                        writer.writerow({'type': 'before',
                                         'test_file': test_filename,
                                         'hash_test_creation': file_time_hash[commit_date],
                                         'test_creation_time': commit_date,
                                         'test_commit_files': file_commit_size[file_time_hash[commit_date]][0],
                                         'test_commit_lines': file_commit_size[file_time_hash[commit_date]][1],
                                         'impl_file': impl_filename,
                                         'hash_impl_creation': file_time_hash[impl_commit_date],
                                         'impl_creation_time': impl_commit_date,
                                         'impl_commit_files': file_commit_size[file_time_hash[impl_commit_date]][0],
                                         'impl_commit_lines': file_commit_size[file_time_hash[impl_commit_date]][1],
                                         })
                    elif commit_date > impl_commit_date:
                        after_count += 1
                        writer.writerow({'type': 'after',
                                         'test_file': test_filename,
                                         'hash_test_creation': file_time_hash[commit_date],
                                         'test_creation_time': commit_date,
                                         'test_commit_files': file_commit_size[file_time_hash[commit_date]][0],
                                         'test_commit_lines': file_commit_size[file_time_hash[commit_date]][1],
                                         'impl_file': impl_filename,
                                         'hash_impl_creation': file_time_hash[impl_commit_date],
                                         'impl_creation_time': impl_commit_date,
                                         'impl_commit_files': file_commit_size[file_time_hash[impl_commit_date]][0],
                                         'impl_commit_lines': file_commit_size[file_time_hash[impl_commit_date]][1],
                                         })
                    else:
                        same_commit_count += 1
                        writer.writerow({'type': 'same',
                                         'test_file': test_filename,
                                         'hash_test_creation': file_time_hash[commit_date],
                                         'test_creation_time': commit_date,
                                         'test_commit_files': file_commit_size[file_time_hash[commit_date]][0],
                                         'test_commit_lines': file_commit_size[file_time_hash[commit_date]][1],
                                         'impl_file': impl_filename,
                                         'hash_impl_creation': file_time_hash[impl_commit_date],
                                         'impl_creation_time': impl_commit_date,
                                         'impl_commit_files': file_commit_size[file_time_hash[impl_commit_date]][0],
                                         'impl_commit_lines': file_commit_size[file_time_hash[impl_commit_date]][1],
                                         })

        return before_count, after_count, same_commit_count

project = sys.argv[1]
# Path to the CSV file - replace with the correct path
csv_file = project + '.csv'

# Perform the analysis
before, after, same_commit = analyze_test_file_creation(csv_file)
with open('./analyseTestfile/results.txt', 'a') as file:
    file.write(project + '\n')
    file.write(f"Test files created before implementation files: {before}\n")
    file.write(f"Test files created after implementation files: {after}\n")
    file.write(f"Test files created in the same commit as implementation files: {same_commit}\n")

# Output the results
print(f"Test files created before implementation files: {before}")
print(f"Test files created after implementation files: {after}")
print(f"Test files created in the same commit as implementation files: {same_commit}")
