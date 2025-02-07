# COMP0104-Coursework2
## File
- `analyse_csv.py` for csv creation
- `collect_information.py` for time analysis, generate `csv` file:
  1. Type of relationship: test file BEFORE/AFTER/SAME implementation file
  2. Hash of commit includes test file
  3. Name of test file
  4. Hash of commit includes implementation file
  5. Name of implementation file

## Execution
`python collect_information.py project_name`
For example, `python collect_information.py knox`, the generated csv file is in `pydrillerData/project_name.csv`

`python analyse_csv.py project_name`
For example, `python analyse_csv.py knox`, the generated csv file is in `analyseTestfile/analyse_project_name.csv`, and the corresponding results are appended to `results.txt`

`run.sh` and `run.bat` are scripts to collect information, analyse and generate results for multiple repositories. Simply change the project name, then the results will output to `results.txt` file.

## Generated Figure
- RQ1
![avatar](/GeneratedImages/Creation_Time_Ratio_Bar.png)
- RQ2 (Choosed 3 specific repos for evidence visualization)
![avatar](/RQ2Diagrams/output1.png)
![avatar](/RQ2Diagrams/output2.png)
![avatar](/RQ2Diagrams/output3.png)
![avatar](/RQ2Diagrams/output4.png)
