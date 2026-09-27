# CSV Data Processing and Automated Report Generator

## Project Description

This project is a Python automation tool that processes student data stored in a CSV file.

The tool automatically reads, cleans, analyzes, and generates a report from the CSV data.

## Features

- Reads student data from a CSV file
- Checks whether the input file exists
- Validates required columns
- Checks for missing values
- Cleans text and numerical data
- Calculates average, highest, and lowest marks
- Calculates average attendance
- Groups students by department
- Identifies students who need attention
- Generates an automated text report
- Saves cleaned data as a new CSV file
- Handles common input and data errors

## Technologies Used

- Python
- Pandas
- CSV
- File Handling

## Project Structure

```text
CSV-Automation-Tool/
│
├── input/
│   └── students.csv
│
├── output/
│   ├── cleaned_students.csv
│   └── student_report.txt
│
├── src/
│   ├── __init__.py
│   └── main.py
│
├── venv/
├── .gitignore
├── README.md
└── requirements.txt
```

## Input

The program accepts a CSV file containing student information.

Required columns:

- Name
- Age
- Department
- Marks
- Attendance

## Output

The program generates:

1. `cleaned_students.csv` — cleaned student data
2. `student_report.txt` — automated analysis report

## Installation

### 1. Clone or download the project

Download this project to your computer and open the project folder in VS Code.

### 2. Create a virtual environment

Open the terminal inside the project folder and run:

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install required libraries

```powershell
pip install -r requirements.txt
```

## How to Run

Make sure the virtual environment is activated.

Run the following command from the project folder:

```powershell
python src/main.py
```

The program will read:

```text
input/students.csv
```

and automatically generate:

```text
output/cleaned_students.csv
output/student_report.txt
```

## Error Handling

The program handles common errors such as:

- Missing input CSV file
- Empty CSV file
- Missing required columns
- Invalid marks or attendance values
- Unable to read the CSV file
## Testing

The project was tested using different input conditions:

| Test Case | Expected Result |
|---|---|
| Valid CSV file | Data is processed successfully |
| Missing CSV file | Error message is displayed |
| Empty CSV file | Error message is displayed |
| Invalid Marks or Attendance | Error message is displayed |
| Missing required column | Error message is displayed |

## Future Improvements

The project can be improved in the future by adding:

- Graphs and charts for data visualization
- Excel file support
- PDF report generation
- A graphical user interface
- Automatic email report delivery
- More advanced data validation
## Author

Alff

## Project Type

Python Automation Project