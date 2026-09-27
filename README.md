# Student CSV Automation Tool

A Python-based automation tool that processes student data from CSV files, performs data cleaning and validation, analyzes academic performance, and automatically generates reports.

This project was developed as part of the **GIST Internship – Python Development Track, Task 2 (Intermediate Level)**.

## 📌 Project Overview

The Student CSV Automation Tool reduces manual work involved in processing student records.

It takes a CSV file containing student information, validates and cleans the data, calculates grades, analyzes student performance, and generates multiple output reports automatically.

## ✨ Features

- CSV file loading and processing
- Data cleaning and validation
- Duplicate and data-quality checks
- Numeric validation for student records
- Automatic grade calculation
- Average marks and attendance analysis
- Department-wise statistics
- Top performer identification
- Students needing attention identification
- Configurable performance thresholds
- Cleaned CSV generation
- Automated TXT report generation
- Styled HTML report generation
- Visual charts and summary cards in the HTML report

## 🛠️ Technologies Used

- Python
- Pandas
- CSV
- HTML
- CSS

## 📂 Project Structure

```text
csv_automation_tool/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── input/
│   └── students.csv
│
├── output/
│   ├── cleaned_students.csv
│   ├── student_report.html
│   └── student_report.txt
│
└── src/
    ├── main.py
    └── __init__.py
````

## 📊 Input Data

The input CSV file should contain the following columns:

* Name
* Age
* Department
* Marks
* Attendance

Example:

```text
Name,Age,Department,Marks,Attendance
Aisha,20,CSE,85,92
Rahul,21,AI&DS,72,81
Sara,20,ECE,58,68
```

## ⚙️ How It Works

The application follows these steps:

1. Loads the student CSV file.
2. Validates the required columns and data.
3. Cleans student information.
4. Checks for invalid or missing numeric values.
5. Detects duplicate records.
6. Calculates grades based on marks.
7. Analyzes marks and attendance.
8. Identifies top-performing students.
9. Identifies students who need attention.
10. Generates cleaned data and automated reports.

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/SyedaJuveriya/csv-automation-tool.git
cd csv-automation-tool
```

### 2. Install the required library

```bash
pip install pandas
```

### 3. Add the input CSV

Place your CSV file inside:

```text
input/students.csv
```

### 4. Run the application

```bash
python src/main.py
```

### 5. Check the generated reports

After execution, the following files are generated inside the `output` folder:

```text
cleaned_students.csv
student_report.txt
student_report.html
```

## 📄 Generated Reports

### Cleaned CSV

Contains the processed and cleaned student records.

### Text Report

Provides a simple summary of the analyzed student data.

### HTML Report

Provides a visually formatted report containing:

* Student statistics
* Data quality summary
* Grade distribution
* Department statistics
* Top performers
* Students needing attention
* Performance charts

## 🎯 Project Level

**GIST Internship – Python Development**

**Task 2: Intermediate Python Automation Tool**

## 🎓 Learning Outcomes

Through this project, I practiced:

* Python automation
* Pandas data processing
* CSV handling
* Data validation and cleaning
* Statistical analysis
* Report generation
* HTML/CSS presentation
* File handling
* Building a complete data-processing workflow

## 👩‍💻 Author

**Syeda Juveriya**

B.Tech – Artificial Intelligence & Data Science
