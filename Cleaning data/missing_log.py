import csv

def log_missing_values(csv_file):
    with open(csv_file, "r", encoding="utf-8-sig", newline='') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        missing_counts = {field: 0 for field in fieldnames}
        total_rows = 0

        for row in reader:
            total_rows += 1
            for field in fieldnames:
                value = row.get(field, "")
                if value == "" or value == "N/A":
                    missing_counts[field] += 1

    print(f"Missing values in '{csv_file}':")
    for field, count in missing_counts.items():
        if count > 0:
            print(f"  {field}: {count} missing ({count/total_rows:.2%})")
    print("-" * 40)

    with open("missing_values_log.txt", "a", encoding="utf-8") as logfile:  
        logfile.write(f"Missing values in '{csv_file}':\n")
        for field, count in missing_counts.items():
            if count > 0:
                logfile.write(f"  {field}: {count} missing ({count/total_rows:.2%})\n")
        logfile.write("-" * 40 + "\n")

csv_files = [
    "booking_danang.csv", "booking_hanoi.csv", "booking_hcm.csv", "booking_nhatrang.csv",
    "booking_hue.csv", "booking_brvt.csv", "booking_cantho.csv", "booking_haiphong.csv"
]


for file in csv_files:
    log_missing_values(file) 