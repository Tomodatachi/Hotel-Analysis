
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os
import logging
import re
from io import StringIO
import pyodbc
from datetime import datetime, timedelta

default_args = {
    'owner': 'Luong',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 6),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
DATA_PATH = os.path.expanduser("~/airflow/data/combined_bookings.csv")
CLEANED_PATH = os.path.expanduser("~/airflow/data/cleaned_bookings.csv")

def extract(**context):
    logging.info(f"Reading data from {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    context['ti'].xcom_push(key='raw_data', value=df.to_json())
    logging.info("Extraction complete")


def transform(**context):
    import json
    raw_json = context['ti'].xcom_pull(task_ids='extract', key='raw_data')
    df = pd.read_json(StringIO(raw_json))

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace(r'[^a-z0-9_]', '', regex=True)
    )

# Use the cleaned column name
    df['price_2_adultsnight'] = (
        df['price_2_adultsnight']
        .astype(str)
        .str.replace(r'vnd', '', case=False, regex=True)
        .str.replace(r'[^\d.]', '', regex=True)  # remove commas, spaces, and non-numeric
        .replace('', pd.NA)
    )

#  Convert to float safely
    df['price_2_adultsnight'] = pd.to_numeric(df['price_2_adultsnight'], errors='coerce')
    df['price_2_adultsnight'] = df['price_2_adultsnight'].fillna(df['price_2_adultsnight'].median())

    # Clean Score column: convert to numeric first
    df['score'] = (
        df['score']
        .replace(['', 'None'], pd.NA)
        .astype(str)
        .str.strip()
    )

    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['score'] = df['score'].fillna(df['score'].mean())
    df['cityprovince'] = df['cityprovince'].fillna('Unknown')
    df['stars'] = df['stars'].astype(str).replace(['', 'nan', 'None'], 'Unrated')
    # Normalize 'overall' column to string and strip whitespace
    df['overall'] = df['overall'].astype(str).str.strip().str.lower()

# Drop rows where 'overall' is empty, 'n/a', or missing
    df = df[~df['overall'].isin(['', 'n/a', 'none', 'nan'])]
    df = df.dropna(subset=['overall'])
    df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')
    df['reviews'] = df['reviews'].fillna(df['reviews'].median())
    df['reviews'] = df['reviews'].astype('int')

    df['check_in'] = df['check_in'].astype(str).str.strip()
    df['check_out'] = df['check_out'].astype(str).str.strip()


    # Clean and standardize
    df = df.drop_duplicates()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace(r'[^a-z0-9_]', '', regex=True)
    )

    context['ti'].xcom_push(key='cleaned_data', value=df.to_json())
def load(**context):

    # Pull cleaned data from XCom
    cleaned_json = context['ti'].xcom_pull(task_ids='transform', key='cleaned_data')
    df = pd.read_json(StringIO(cleaned_json))

    # Connect to SQL Server
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=[censored for privacy];'
        'DATABASE=BookingDB;'
        'UID=[censored for privacy];'
        'PWD=[censored for privacy];'
        'Encrypt=no;'
        'TrustServerCertificate=yes;'
        'Connection Timeout=30;'
    )
    cursor = conn.cursor()
    df.rename(columns={
        'check_in': 'checkin',
        'check_out': 'checkout'
    }, inplace=True)

    # Insert rows
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO CleanedBookings (
                stay, cityprovince, price_2_adultsnight, checkin, checkout,
                score, stars, address, reviews, overall, link
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row['stay'], row['cityprovince'], row['price_2_adultsnight'], row['checkin'], row['checkout'],
            row['score'], row['stars'], row['address'], row['reviews'], row['overall'], row['link'])

    conn.commit()
    cursor.close()
    conn.close()


with DAG(
    'booking_etl',
    default_args=default_args,
    description='ETL pipeline for booking data',
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract_task = PythonOperator(task_id='extract', python_callable=extract)
    transform_task = PythonOperator(task_id='transform', python_callable=transform)
    load_task = PythonOperator(task_id='load', python_callable=load)

    extract_task >> transform_task >> load_task
