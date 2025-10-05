import csv
import re

def clean_score_column(csv_file):
    rows = []
    with open(csv_file, "r", encoding="utf-8-sig", newline='') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        for row in reader:
            score = row.get("Score", "")
            # Extract numeric score using regex
            match = re.search(r"(\d+\.\d+)", score)
            if match:
                row["Score"] = float(match.group(1))
            else:
                row["Score"] = ""
            rows.append(row)

    with open(csv_file, "w", encoding="utf-8-sig", newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
def clean_price_column(csv_file):
    rows = []
    with open(csv_file, "r", encoding="utf-8-sig", newline='') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        for row in reader:
            price = row.get("Price (2 adults/night)", "")
            # Extract numeric price using regex
            match = re.search(r"(\d+)", price.replace(",", ""))
            if match:
                row["Price (2 adults/night)"] = float(match.group(1))
            else:
                row["Price (2 adults/night)"] = ""
            rows.append(row)

    with open(csv_file, "w", encoding="utf-8-sig", newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def clean_reviews_column(csv_file):
    rows = []
    with open(csv_file, "r", encoding="utf-8-sig", newline='') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        for row in reader:
            reviews = row.get("Reviews", "")
            # Extract numeric reviews using regex
            match = re.search(r"(\d+)", reviews.replace(",", ""))
            if match:
                row["Reviews"] = int(match.group(1))
            else:
                row["Reviews"] = ""
            rows.append(row)

    with open(csv_file, "w", encoding="utf-8-sig", newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def clean_csv_data(csv_file):
    clean_score_column(csv_file)
    clean_price_column(csv_file)
    clean_reviews_column(csv_file)

csv_file = str(input("Enter the CSV file name (with .csv extension): "))
clean_csv_data(csv_file)
