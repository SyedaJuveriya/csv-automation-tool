import pandas as pd
import os


# Function to load the CSV file
def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        print("Please add data to the CSV file.")
        exit()

    except Exception as error:
        print("Error: Unable to read the CSV file.")
        print("Details:", error)
        exit()


# Function to clean the data
def clean_data(data):

    # Remove completely empty rows
    data = data.dropna(how="all")

    # Remove extra spaces from text columns
    data["Name"] = data["Name"].str.strip()
    data["Department"] = data["Department"].str.strip()

    # Convert Marks and Attendance into numbers
    data["Marks"] = pd.to_numeric(
        data["Marks"],
        errors="coerce"
    )

    data["Attendance"] = pd.to_numeric(
        data["Attendance"],
        errors="coerce"
    )

    # Check for invalid numeric data
    if data["Marks"].isnull().any() or data["Attendance"].isnull().any():
        print("Error: Marks or Attendance contains invalid data.")
        print("Please make sure Marks and Attendance contain numbers only.")
        exit()

    return data


# Function to analyze the data
def analyze_data(data):

    total_students = len(data)

    average_marks = data["Marks"].mean()

    highest_marks = data["Marks"].max()

    lowest_marks = data["Marks"].min()

    average_attendance = data["Attendance"].mean()

    department_counts = data["Department"].value_counts()

    # Find students who need attention
    students_need_attention = data[
        (data["Marks"] < 60) | (data["Attendance"] < 75)
    ]

    return (
        total_students,
        average_marks,
        highest_marks,
        lowest_marks,
        average_attendance,
        department_counts,
        students_need_attention
    )


# Function to generate the report
def generate_report(
    total_students,
    average_marks,
    highest_marks,
    lowest_marks,
    average_attendance,
    department_counts,
    students_need_attention
):

    report_path = "output/student_report.txt"

    with open(report_path, "w") as report:

        report.write("STUDENT DATA AUTOMATION REPORT\n")
        report.write("=" * 40 + "\n\n")

        report.write(f"Total Students: {total_students}\n")
        report.write(f"Average Marks: {average_marks:.2f}\n")
        report.write(f"Highest Marks: {highest_marks}\n")
        report.write(f"Lowest Marks: {lowest_marks}\n")
        report.write(
            f"Average Attendance: {average_attendance:.2f}%\n\n"
        )

        report.write("Students by Department:\n")

        for department, count in department_counts.items():
            report.write(f"{department}: {count}\n")

        report.write("\n")

        report.write("Students Needing Attention:\n")

        if len(students_need_attention) == 0:
            report.write("No students need attention.\n")

        else:
            report.write(
                students_need_attention[
                    ["Name", "Marks", "Attendance"]
                ].to_string(index=False)
            )

    return report_path


# Function to save cleaned data
def save_cleaned_data(data):

    cleaned_file_path = "output/cleaned_students.csv"

    data.to_csv(cleaned_file_path, index=False)

    return cleaned_file_path


# Main function
def main():

    # Input CSV file path
    file_path = "input/students.csv"

    # Create output folder if it does not exist
    os.makedirs("output", exist_ok=True)

    # Check if the input file exists
    if not os.path.exists(file_path):
        print("Error: The input CSV file was not found.")
        print("Please place students.csv inside the input folder.")
        exit()

    # Load the CSV file
    data = load_csv(file_path)

    # Check required columns
    required_columns = [
        "Name",
        "Age",
        "Department",
        "Marks",
        "Attendance"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        print("Error: Required columns are missing.")
        print("Missing columns:", missing_columns)
        exit()

    print("CSV file loaded successfully!")
    print()

    print("Number of students:", len(data))
    print()

    print("Columns in the CSV:")
    print(data.columns.tolist())
    print()

    # Show missing values before cleaning
    print("Missing values before cleaning:")
    print(data.isnull().sum())
    print()

    # Clean the data
    data = clean_data(data)

    print("Data cleaning completed!")
    print()

    # Show missing values after cleaning
    print("Missing values after cleaning:")
    print(data.isnull().sum())

    # Analyze the data
    (
        total_students,
        average_marks,
        highest_marks,
        lowest_marks,
        average_attendance,
        department_counts,
        students_need_attention
    ) = analyze_data(data)

    print()
    print("===== STUDENT ANALYSIS =====")

    print("Total students:", total_students)

    print("Average marks:", round(average_marks, 2))

    print("Highest marks:", highest_marks)

    print("Lowest marks:", lowest_marks)

    print("Average attendance:", round(average_attendance, 2))

    print()
    print("Students by department:")
    print(department_counts)

    print()
    print("===== STUDENTS NEEDING ATTENTION =====")

    if len(students_need_attention) == 0:
        print("No students need attention.")

    else:
        print(
            students_need_attention[
                ["Name", "Marks", "Attendance"]
            ]
        )

    # Generate the report
    report_path = generate_report(
        total_students,
        average_marks,
        highest_marks,
        lowest_marks,
        average_attendance,
        department_counts,
        students_need_attention
    )

    print()
    print("Report generated successfully!")
    print("Report saved to:", report_path)

    # Save cleaned data
    cleaned_file_path = save_cleaned_data(data)

    print("Cleaned CSV saved to:", cleaned_file_path)

    # Final success message
    print()
    print("========================================")
    print("AUTOMATION COMPLETED SUCCESSFULLY")
    print("========================================")
    print("Input file:", file_path)
    print("Report file:", report_path)
    print("Cleaned file:", cleaned_file_path)


# Program starting point
if __name__ == "__main__":
    main()