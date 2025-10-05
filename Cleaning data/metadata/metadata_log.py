import csv

def infer_type(value):
    if value == "" or value == "N/A":
        return "missing"
    try:
        int(value)
        return "int"
    except ValueError:
        try:
            float(value)
            return "float"
        except ValueError:
            return "str"

def export_metadata_log(csv_files, output_file):
    with open(output_file, "w", encoding="utf-8") as log:
        for csv_file in csv_files:
            with open(csv_file, "r", encoding="utf-8-sig", newline='') as infile:
                reader = csv.DictReader(infile)
                fieldnames = reader.fieldnames
                rows = list(reader)
                num_rows = len(rows)
                num_cols = len(fieldnames)
                log.write(f"Metadata for '{csv_file}':\n")
                log.write(f"  Number of rows: {num_rows}\n")
                log.write(f"  Number of columns: {num_cols}\n")
                log.write(f"  Columns:\n")
                for field in fieldnames:
                    # Infer type from first non-missing value
                    dtype = "missing"
                    for row in rows:
                        val = row.get(field, "")
                        dtype = infer_type(val)
                        if dtype != "missing":
                            break
                    log.write(f"    - {field}: {dtype}\n")
                log.write("-" * 40 + "\n")

csv_files = [
    "booking_danang.csv", "booking_hanoi.csv", "booking_hcm.csv", "booking_nhatrang.csv",
    "booking_hue.csv", "booking_brvt.csv", "booking_cantho.csv", "booking_haiphong.csv"
]

export_metadata_log(csv_files, "metadata_log.txt")
