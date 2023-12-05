# COMP0104-Coursework2
## File
- `analyse_csv.py` for csv creation
- `collectInformation.py` for time analysis, generate `csv` file:
  1. Type of relationship: test file BEFORE/AFTER/SAME implementation file
  2. Hash of commit includes test file
  3. Name of test file
  4. Hash of commit includes implementation file
  5. Name of implementation file

## Execution
`python collectInformation.py project_name`
For example, `python collectInformation.py knox`, the generated csv file is in `pydrillerData/project_name.csv`

`python analyse_csv.py project_name`
For example, `python analyse_csv.py knox`, the generated csv file is in `pydrillerData/analyse_project_name.csv`, and the corresponding results are appended to `results.txt`

`run.sh` and `run.bat` are scripts to collect information, analyse and generate results for multiple repositories. Simply change the project name, then the results will output to `results.txt` file.