from pydriller import Repository
import csv

with open('./pydrillerData/my.csv', 'w', newline='') as file:
    fields = ['msg', 'files', 'lines', 'committer_date', 'modified_files', 'merge']
    writer = csv.DictWriter(file, fieldnames = fields)
    for commit in Repository('https://github.com/yuawn/NTU-Computer-Security', only_in_branch='master').traverse_commits():
        modified_file = []
        for file in commit.modified_files:
            modified_file.append(file.filename)
        writer.writerow({'msg': commit.msg, 'files': commit.files, 'lines': commit.lines, 'committer_date': commit.committer_date, 'modified_files': modified_file, 'merge': commit.merge})