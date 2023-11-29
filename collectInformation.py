from pydriller import Repository
import csv

with open('./pydrillerData/my.csv', 'w', newline='') as file:
    fields = ['msg', 'files', 'lines', 'committer_date', 'modified_files', 'merge', 'branches']
    writer = csv.DictWriter(file, fieldnames = fields)
    writer.writerow({'msg': 'msg', 'files': 'files', 'lines': 'lines', 'committer_date': 'committer_date', 'modified_files': 'modified_file', 'merge': 'merge', 'branches': 'branches'})
    for commit in Repository('https://github.com/apache/iceberg').traverse_commits():
        modified_file = []
        branches = []
        for file in commit.modified_files:
            modified_file.append(file.filename)
        for branch in commit.branches:
            branches.append(branch)
        writer.writerow({'msg': commit.msg, 'files': commit.files, 'lines': commit.lines, 'committer_date': commit.committer_date, 'modified_files': modified_file, 'merge': commit.merge, 'branches': branches})