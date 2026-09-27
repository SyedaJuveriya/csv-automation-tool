import argparse
import html
import os
import pandas as pd

DEFAULT_INPUT = "input/students.csv"
DEFAULT_OUTPUT = "output"
DEFAULT_PASS_MARKS = 60
DEFAULT_MIN_ATTENDANCE = 75
DEFAULT_TOP_N = 3
REQUIRED_COLUMNS = ["Name", "Age", "Department", "Marks", "Attendance"]
GRADE_ORDER = ["A", "B", "C", "D", "F"]
GRADE_COLORS = {"A": "#16a34a", "B": "#2563eb", "C": "#ca8a04", "D": "#ea580c", "F": "#dc2626"}


def load_csv(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input CSV file was not found: {path}")
    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty. Please add student data.")
    except Exception as e:
        raise ValueError(f"Unable to read the CSV file: {e}")


def validate_columns(data):
    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        raise ValueError("Required columns are missing: " + ", ".join(missing))


def clean_data(data):
    data = data.copy()
    original = len(data)
    data = data.dropna(how="all").copy()
    empty_removed = original - len(data)

    data["Name"] = data["Name"].astype("string").str.strip()
    data["Department"] = data["Department"].astype("string").str.strip()
    for col in ["Age", "Marks", "Attendance"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    missing_found = int(data[REQUIRED_COLUMNS].isna().sum().sum())
    invalid_required = data[REQUIRED_COLUMNS].isna().any(axis=1)
    invalid_age = (data["Age"] < 0) | (data["Age"] > 120)
    invalid_marks = (data["Marks"] < 0) | (data["Marks"] > 100)
    invalid_attendance = (data["Attendance"] < 0) | (data["Attendance"] > 100)

    invalid = invalid_required | invalid_age.fillna(False) | invalid_marks.fillna(False) | invalid_attendance.fillna(False)
    invalid_removed = int(invalid.sum())
    data = data.loc[~invalid].copy()

    duplicates = int(data.duplicated().sum())
    data = data.drop_duplicates().copy()

    if data.empty:
        raise ValueError("No valid student records remain after cleaning.")

    quality = {
        "original": original,
        "empty_removed": empty_removed,
        "missing_found": missing_found,
        "invalid_removed": invalid_removed,
        "duplicates_removed": duplicates,
        "final": len(data),
    }
    return data, quality


def calculate_grade(marks, pass_marks):
    if marks >= 90:
        return "A"
    if marks >= 75:
        return "B"
    if marks >= pass_marks:
        return "C"
    if marks >= 40:
        return "D"
    return "F"


def add_grades(data, pass_marks):
    data = data.copy()
    data["Grade"] = data["Marks"].apply(lambda x: calculate_grade(x, pass_marks))
    return data


def analyze(data, pass_marks, min_attendance, top_n):
    attention = data[(data["Marks"] < pass_marks) | (data["Attendance"] < min_attendance)].copy()
    top = data.sort_values(["Marks", "Attendance", "Name"], ascending=[False, False, True]).head(top_n)
    grades = data["Grade"].value_counts().reindex(GRADE_ORDER, fill_value=0)

    return {
        "total": len(data),
        "avg_marks": data["Marks"].mean(),
        "highest": data["Marks"].max(),
        "lowest": data["Marks"].min(),
        "avg_attendance": data["Attendance"].mean(),
        "departments": data["Department"].value_counts(),
        "attention": attention,
        "top": top,
        "grades": grades,
    }


def generate_text_report(a, q, pass_marks, min_attendance, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("STUDENT DATA AUTOMATION REPORT\n" + "=" * 45 + "\n\n")
        f.write("DATA QUALITY SUMMARY\n" + "-" * 45 + "\n")
        f.write(f"Original records: {q['original']}\n")
        f.write(f"Empty rows removed: {q['empty_removed']}\n")
        f.write(f"Missing values found: {q['missing_found']}\n")
        f.write(f"Invalid records removed: {q['invalid_removed']}\n")
        f.write(f"Duplicate records removed: {q['duplicates_removed']}\n")
        f.write(f"Records after cleaning: {q['final']}\n\n")

        f.write("CLASS SUMMARY\n" + "-" * 45 + "\n")
        f.write(f"Total Students: {a['total']}\n")
        f.write(f"Average Marks: {a['avg_marks']:.2f}\n")
        f.write(f"Highest Marks: {a['highest']:g}\n")
        f.write(f"Lowest Marks: {a['lowest']:g}\n")
        f.write(f"Average Attendance: {a['avg_attendance']:.2f}%\n")
        f.write(f"Passing Marks: {pass_marks:g}\n")
        f.write(f"Minimum Attendance: {min_attendance:g}%\n\n")

        f.write("STUDENTS BY DEPARTMENT\n" + "-" * 45 + "\n")
        for dept, count in a["departments"].items():
            f.write(f"{dept}: {count}\n")

        f.write("\nGRADE DISTRIBUTION\n" + "-" * 45 + "\n")
        for grade, count in a["grades"].items():
            f.write(f"{grade}: {count}\n")

        f.write("\nTOP PERFORMERS\n" + "-" * 45 + "\n")
        f.write(a["top"][["Name", "Marks", "Grade"]].to_string(index=False) + "\n\n")

        f.write("STUDENTS NEEDING ATTENTION\n" + "-" * 45 + "\n")
        if a["attention"].empty:
            f.write("No students need attention.\n")
        else:
            f.write(a["attention"][["Name", "Marks", "Attendance"]].to_string(index=False) + "\n")


def generate_html_report(a, q, pass_marks, min_attendance, path):
    dept_rows = "".join(
        f"<tr><td>{html.escape(str(dept))}</td><td>{int(count)}</td></tr>"
        for dept, count in a["departments"].items()
    )
    top_rows = "".join(
        f"<tr><td>{html.escape(str(r['Name']))}</td><td>{r['Marks']:g}</td>"
        f"<td class='grade-{r['Grade']}'>{r['Grade']}</td></tr>"
        for _, r in a["top"].iterrows()
    )
    attention_rows = "".join(
        f"<tr><td>{html.escape(str(r['Name']))}</td><td>{r['Marks']:g}</td>"
        f"<td class='low'>{r['Attendance']:g}%</td></tr>"
        for _, r in a["attention"].iterrows()
    ) or "<tr><td colspan='3' class='success'>No students need attention.</td></tr>"

    max_count = max(int(a["grades"].max()), 1)
    bars = ""
    for grade, count in a["grades"].items():
        count = int(count)
        height = max(int(count / max_count * 170), 4) if count else 4
        bars += (
            f"<div class='bar-wrap'><div class='bar-count'>{count}</div>"
            f"<div class='bar' style='height:{height}px;background:{GRADE_COLORS[grade]}'></div>"
            f"<div class='bar-label'>{grade}</div></div>"
        )

    qcards = "".join(
        f"<div class='qcard'><span>{label}</span><strong>{value}</strong></div>"
        for label, value in [
            ("Original Records", q["original"]),
            ("Duplicates Removed", q["duplicates_removed"]),
            ("Invalid Removed", q["invalid_removed"]),
            ("Final Records", q["final"]),
        ]
    )

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Student Data Automation Report</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;padding:40px;font-family:"Segoe UI",Arial,sans-serif;background:radial-gradient(circle at 8% 8%,rgba(99,102,241,.16),transparent 28%),radial-gradient(circle at 92% 18%,rgba(168,85,247,.14),transparent 30%),linear-gradient(135deg,#eef2ff 0%,#f8fafc 48%,#f5f3ff 100%);color:#1f2937;min-height:100vh}}
.container{{max-width:1250px;margin:auto}}
.header{{position:relative;overflow:hidden;background:linear-gradient(135deg,#4338ca 0%,#6366f1 48%,#7c3aed 100%);color:#fff;border-radius:20px;padding:38px;margin-bottom:28px;box-shadow:0 14px 35px rgba(79,70,229,.22);transition:transform .25s,box-shadow .25s}}
.header:hover{{transform:translateY(-2px);box-shadow:0 18px 40px rgba(79,70,229,.28)}}
.header:after{{content:"";position:absolute;width:220px;height:220px;border-radius:50%;right:-70px;top:-100px;background:rgba(255,255,255,.1)}}
.header h1{{margin:0 0 8px;font-size:34px}} .header p{{margin:0;opacity:.9}}
.stats,.qgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:18px;margin-bottom:28px}}
.card,.section{{background:rgba(255,255,255,.9);backdrop-filter:blur(8px);border:1px solid rgba(99,102,241,.12);box-shadow:0 8px 25px rgba(15,23,42,.06);border-radius:18px;transition:transform .25s,box-shadow .25s,border-color .25s}}
.card{{padding:22px}} .card:hover{{transform:translateY(-6px);box-shadow:0 15px 30px rgba(79,70,229,.14);border-color:rgba(99,102,241,.3)}}
.card h3{{margin:0;font-size:14px;color:#6b7280}} .card p{{margin:9px 0 0;font-size:27px;font-weight:700}}
.section{{padding:26px;margin-bottom:28px}} .section:hover{{transform:translateY(-2px);box-shadow:0 12px 30px rgba(79,70,229,.09)}} .section h2{{margin-top:0;color:#374151}} .subtitle{{color:#6b7280;margin-top:-8px}}
.qgrid{{margin:18px 0 0}} .qcard{{background:linear-gradient(145deg,#fff,#f8f7ff);border:1px solid #e2e8f0;border-radius:13px;padding:18px;transition:transform .22s,box-shadow .22s}} .qcard:hover{{transform:translateY(-4px);box-shadow:0 9px 20px rgba(79,70,229,.1)}}
.qcard span{{display:block;color:#64748b;font-size:13px;margin-bottom:7px}} .qcard strong{{font-size:22px}}
.badges{{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}} .badge{{display:inline-block;padding:9px 14px;border-radius:999px;background:linear-gradient(135deg,#eef2ff,#f5f3ff);color:#4338ca;border:1px solid #c7d2fe;font-size:13px;font-weight:600;transition:transform .2s,box-shadow .2s}} .badge:hover{{transform:translateY(-2px);box-shadow:0 5px 12px rgba(79,70,229,.12)}}
.chart{{display:flex;align-items:flex-end;justify-content:center;gap:42px;min-height:250px;padding:28px 20px 18px;background:linear-gradient(135deg,#f8f7ff,#eef2ff);border-radius:14px;border:1px solid #e0e7ff}}
.bar-wrap{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:210px}} .bar-count{{font-size:13px;font-weight:700;margin-bottom:7px}}
.bar{{width:55px;min-height:4px;border-radius:8px 8px 2px 2px;transition:transform .25s,opacity .25s,filter .25s;box-shadow:0 5px 12px rgba(15,23,42,.12)}} .bar:hover{{transform:translateY(-7px) scaleX(1.08);opacity:.88;filter:brightness(1.08)}}
.bar-label{{margin-top:9px;font-weight:700;color:#475569}}
table{{width:100%;border-collapse:separate;border-spacing:0;overflow:hidden;border-radius:12px;box-shadow:0 3px 12px rgba(15,23,42,.04)}} th{{text-align:left;padding:13px 15px;background:#4f46e5;color:#fff}} td{{padding:14px 15px;border-bottom:1px solid #e5e7eb;transition:background-color .2s,padding-left .2s}} tr:hover td{{background:#eef2ff}} tr:hover td:first-child{{padding-left:20px}}
.grade-A{{color:#16a34a;font-weight:700}} .grade-B{{color:#2563eb;font-weight:700}} .grade-C{{color:#ca8a04;font-weight:700}} .grade-D{{color:#ea580c;font-weight:700}} .grade-F{{color:#dc2626;font-weight:700}} .low{{color:#dc2626;font-weight:600}}
.success{{color:#16a34a;font-weight:600;text-align:center}} .footer{{text-align:center;color:#64748b;font-size:13px;margin-top:30px}}
@media(max-width:700px){{body{{padding:18px}}.header h1{{font-size:27px}}.chart{{gap:16px}}.bar{{width:40px}}}}
</style>
</head>
<body><div class="container">
<div class="header"><h1>Student Data Automation Report</h1><p>Generated automatically by Student CSV Automation Tool</p></div>
<div class="stats">
<div class="card"><h3>Total Students</h3><p>{a["total"]}</p></div>
<div class="card"><h3>Average Marks</h3><p>{a["avg_marks"]:.2f}</p></div>
<div class="card"><h3>Highest Marks</h3><p>{a["highest"]:g}</p></div>
<div class="card"><h3>Lowest Marks</h3><p>{a["lowest"]:g}</p></div>
<div class="card"><h3>Average Attendance</h3><p>{a["avg_attendance"]:.2f}%</p></div>
</div>
<div class="section"><h2>Data Quality Summary</h2><p class="subtitle">Automatic validation, cleaning and duplicate detection.</p>
<div class="qgrid">{qcards}</div>
<div class="badges"><span class="badge">Passing Marks: {pass_marks:g}</span><span class="badge">Minimum Attendance: {min_attendance:g}%</span></div>
</div>
<div class="section"><h2>Grade Distribution</h2><div class="chart">{bars}</div></div>
<div class="section"><h2>Students by Department</h2><table><tr><th>Department</th><th>Count</th></tr>{dept_rows}</table></div>
<div class="section"><h2>Top Performers</h2><table><tr><th>Name</th><th>Marks</th><th>Grade</th></tr>{top_rows}</table></div>
<div class="section"><h2>Students Needing Attention</h2><p class="subtitle">Students below the marks or attendance thresholds.</p>
<table><tr><th>Name</th><th>Marks</th><th>Attendance</th></tr>{attention_rows}</table></div>
<div class="footer">Student CSV Automation Tool • Automated data cleaning, analysis and report generation</div>
</div></body></html>"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def parse_args():
    parser = argparse.ArgumentParser(description="Automate student CSV cleaning, analysis and reporting.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help=f"Input CSV path (default: {DEFAULT_INPUT})")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT, help=f"Output folder (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--pass-marks", type=float, default=DEFAULT_PASS_MARKS, help="Passing marks (0-100).")
    parser.add_argument("--min-attendance", type=float, default=DEFAULT_MIN_ATTENDANCE, help="Minimum attendance percentage (0-100).")
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N, help="Number of top performers.")
    return parser.parse_args()


def main():
    args = parse_args()

    if not 0 <= args.pass_marks <= 100:
        raise ValueError("Passing marks must be between 0 and 100.")
    if not 0 <= args.min_attendance <= 100:
        raise ValueError("Minimum attendance must be between 0 and 100.")
    if args.top_n < 1:
        raise ValueError("Top N must be at least 1.")

    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 55)
    print("       STUDENT CSV AUTOMATION TOOL")
    print("=" * 55)
    print(f"\nInput file: {args.input}")

    data = load_csv(args.input)
    validate_columns(data)
    print(f"CSV file loaded successfully! Records found: {len(data)}")

    data, quality = clean_data(data)
    print("Data cleaning completed!")
    print(f"Duplicates removed: {quality['duplicates_removed']}")
    print(f"Invalid records removed: {quality['invalid_removed']}")
    print(f"Valid records remaining: {len(data)}")

    data = add_grades(data, args.pass_marks)
    analysis = analyze(data, args.pass_marks, args.min_attendance, args.top_n)

    print(f"\nAverage marks: {analysis['avg_marks']:.2f}")
    print(f"Average attendance: {analysis['avg_attendance']:.2f}%")
    print("\n===== TOP PERFORMERS =====")
    print(analysis["top"][["Name", "Marks", "Grade"]].to_string(index=False))
    print("\n===== STUDENTS NEEDING ATTENTION =====")
    if analysis["attention"].empty:
        print("No students need attention.")
    else:
        print(analysis["attention"][["Name", "Marks", "Attendance"]].to_string(index=False))

    report = os.path.join(args.output_dir, "student_report.txt")
    html_report = os.path.join(args.output_dir, "student_report.html")
    cleaned = os.path.join(args.output_dir, "cleaned_students.csv")

    generate_text_report(analysis, quality, args.pass_marks, args.min_attendance, report)
    generate_html_report(analysis, quality, args.pass_marks, args.min_attendance, html_report)
    data.to_csv(cleaned, index=False)

    print("\n===== AUTOMATION COMPLETED SUCCESSFULLY =====")
    print(f"Text report: {report}")
    print(f"HTML report: {html_report}")
    print(f"Cleaned CSV: {cleaned}")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError) as e:
        print(f"\nError: {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        raise SystemExit(1)
