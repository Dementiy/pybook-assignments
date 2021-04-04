import psycopg2
import csv

conn = psycopg2.connect("host=localhost port=5433 dbname=odscourse user=postgres password=secret")
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS telecom_churn (
    id SERIAL PRIMARY KEY,
    state VARCHAR,
    account_length INTEGER,
    area_code INTEGER,
    international_plan VARCHAR,
    voice_mail_plan VARCHAR,
    number_vmail_messages INTEGER,
    total_day_minutes REAL,
    total_day_calls INTEGER,
    total_day_charge REAL,
    total_eve_minutes REAL,
    total_eve_calls INTEGER,
    total_eve_charge REAL,
    total_night_minutes REAL,
    total_night_calls INTEGER,
    total_night_charge REAL,
    total_intl_minutes REAL,
    total_intl_calls INTEGER,
    total_intl_charge REAL,
    customer_service_calls INTEGER,
    churn BOOLEAN
)
"""
cursor.execute(query)
conn.commit()

with open('telecom_churn.csv', 'r') as f:
    reader = csv.reader(f)
    # Skip the header row
    next(reader)
    for Id, row in enumerate(reader):
        cursor.execute(
            "INSERT INTO telecom_churn VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [Id] + row
        )
conn.commit()
