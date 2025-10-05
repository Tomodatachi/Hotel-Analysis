import csv
import os

def export_missing_indices(csv_file):
    report_file = os.path.splitext(csv_file)[0] + "_missing_report.txt"
    with open(csv_file, "r", encoding="utf-8-sig", newline='') as infile, \
         open(report_file, "w", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        missing_by_row = {}
        for idx, row in enumerate(reader, start=2):  # start=2 to account for header row
            missing_fields = []
            for field in fieldnames:
                value = row.get(field, "")
                if value == "" or value == "N/A":
                    missing_fields.append(field)
            if missing_fields:
                missing_by_row[idx] = missing_fields
        outfile.write(f"Missing value indices for '{csv_file}':\n")
        for idx in missing_by_row:
            columns = ", ".join(missing_by_row[idx])
            outfile.write(f"  Row {idx}: {columns}\n")
        outfile.write("-" * 40 + "\n")

csv_files = [
    "booking_danang.csv", "booking_hanoi.csv", "booking_hcm.csv", "booking_nhatrang.csv",
    "booking_hue.csv", "booking_brvt.csv", "booking_cantho.csv", "booking_haiphong.csv"
]

for file in csv_files:
    export_missing_indices(file)
