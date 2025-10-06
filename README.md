# 🏨 Hotel Analysis

This project explores how hotel prices, ratings, and location data interact — uncovering patterns that influence cost and quality across different regions.

---

## 📌 Project Goals

- Analyze hotel booking data from Booking.com
- Clean and transform raw data using an Airflow ETL pipeline
- Load structured data into SQL Server for analysis
- Discover relationships between price, reviews, ratings, and location

---

## 🛠️ Tech Stack

| Tool         | Purpose                        |
|--------------|--------------------------------|
| Python       | Data processing and ETL logic  |
| Pandas       | Data cleaning and transformation |
| Airflow      | Workflow orchestration         |
| SQL Server   | Data storage and querying      |
| GitHub       | Version control and collaboration |

---

## 📂 Folder Structure
<pre>
Hotel-Analysis/ 
├── Booking.com's data                              # Raw CSV files scrapped from Booking.com
   ├── README.md                                    # Some description of this folder
   ├── Requirements.txt                             # Version of Selenium used
   ├── Scrapping_code.py                            # Python code for scrapping data
   ├── booking_(...).csv                            # Raw CSV files of scrapped data of (...) cities on Booking.com
├── Cleaning data                                   # Processing data
   ├── Missing values detection
      ├── booking_(...)_missing_report.txt          # Details of missing values from raw data
      ├── missing_detail.py                         # Python program for missing value detection in detail
      ├── missing_log.py                            # Python counting program to export a statistic file of missing values
      ├── missing_values_log.txt                    # Log file exported from counting program above
   ├── data
      ├── booking_(...).csv                         # All CSV files after re-edit some changes for later easier use
      ├── great_data.py                             # Python code to combined all CSV files above into one great data file
      ├── combined_bookings.csv                     # The great file of data containing information from CSV files above
      ├── booking_etl_dag.py                        # Python program to write DAG and ETL method inserted to Apache Airflow
      ├── cleaned_bookings.csv                      # The great file of cleaned data using Apache Airflow
   ├── metadata
      ├── metadata_log.py                           # Python code to export metadata of CSV files
      ├── metadata_log.txt                          # A report of metadata of CSV files
   ├── Cleaning_code.py                             # The code for re-edit raw CSV files into CSV files in "data" folder
├── README.md                                       # Project overview
</pre>
---

## 🚀 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/Tomodatachi/Hotel-Analysis.git
2. Set up your Airflow DAG using booking_etl_dag.py
3. Ensure Mircrosoft SQL Server is running and accessible
4. Trigger the DAG to extract, transform, and load the data

## 📊 Insights You Can Explore

- Which cities offer the best value for money?
- Do higher review counts correlate with better ratings?
- How do prices vary by province or season?

👤 Contributors
- Lương Minh Ngọc              # Project Leader | ETL Developer | Data Scraper & Cleaner
- Nguyễn Minh Hoàng            # Project Member | Data Checker & Analyst
- Hồ Nhật Tân                  # Project Member | Idea Maker | Data Checker & Analyst
- Nguyễn Viết Hưng             # Project Member | Data Checker & Analyst
