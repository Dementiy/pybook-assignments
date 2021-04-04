import psycopg2
import psycopg2.extras
from pprint import pprint as pp
from tabulate import tabulate

conn = psycopg2.connect("host=localhost port=5433 dbname=odscourse user=postgres password=secret")
cursor = conn.cursor() # cursor_factory=psycopg2.extras.DictCursor)

def fetch_all(cursor):
    colnames = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return [{colname:value for colname, value in zip(colnames, record)} for record in records]


cursor.execute("SELECT * FROM telecom_churn LIMIT 5")
records = cursor.fetchall()
print(records)


cursor.execute(
    """
    SELECT churn, COUNT(*)
        FROM telecom_churn
        GROUP BY churn
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute(
    """
    SELECT area_code, ROUND((COUNT(*) / (SELECT COUNT(*) FROM telecom_churn)::numeric), 6)
        FROM telecom_churn
        GROUP BY area_code;
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("SELECT * FROM telecom_churn ORDER BY total_day_charge DESC LIMIT 5")
records = cursor.fetchall()
print(records)

cursor.execute("SELECT * FROM telecom_churn ORDER BY churn ASC, total_day_charge DESC LIMIT 5")
records = cursor.fetchall()
print(records)

cursor.execute("SELECT AVG(churn::int) FROM telecom_churn")
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("""
    SELECT AVG(account_length), AVG(number_vmail_messages), AVG(total_day_minutes), AVG(total_day_calls),
              AVG(total_day_charge), AVG(total_eve_minutes), AVG(total_eve_calls), AVG(total_eve_charge),
              AVG(total_night_minutes), AVG(total_night_calls), AVG(total_night_charge), AVG(total_intl_minutes),
              AVG(total_intl_calls), AVG(total_intl_charge), AVG(customer_service_calls), AVG(churn::int)
        FROM telecom_churn WHERE churn = TRUE
""")
records = cursor.fetchall()
pp(records)


cursor.execute("""
    SELECT AVG(total_day_minutes) FROM telecom_churn WHERE churn = TRUE
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("""
    SELECT MAX(total_intl_minutes) FROM telecom_churn
    WHERE churn = FALSE AND international_plan = 'No'
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("""
    SELECT (CASE WHEN international_plan = 'No' THEN False ELSE True END) as international_plan
    FROM telecom_churn
    LIMIT 5
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("""
    SELECT COUNT(*),
           AVG(total_day_minutes), STDDEV(total_day_minutes), MIN(total_day_minutes),
           PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY total_day_minutes) as "50%", MAX(total_day_minutes)
    FROM telecom_churn
    GROUP BY churn
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("""
    SELECT churn, international_plan, COUNT(*) FROM telecom_churn
    GROUP BY churn, international_plan
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("""
    SELECT area_code,
           AVG(total_day_calls) as avg_total_day_calls,
           AVG(total_eve_calls) as avg_total_eve_calls,
           AVG(total_night_calls) as avg_total_night_calls
    FROM telecom_churn
    GROUP BY area_code
    ORDER BY area_code
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("""
    CREATE TABLE telecom_churn_temp  AS
        SELECT *, (total_day_calls + total_eve_calls + total_night_calls + total_intl_calls) as total_calls
        FROM telecom_churn
        LIMIT 5;
    SELECT total_calls FROM telecom_churn_temp
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("""
    CREATE EXTENSION tablefunc;
    SELECT Churn, SUM(No) as No, SUM(Yes) as Yes, SUM(No+Yes) as "All" FROM (SELECT *
    FROM crosstab('SELECT churn, international_plan, COUNT(*)::int FROM telecom_churn GROUP BY churn, international_plan ORDER BY 1,2')
    AS (Churn BOOLEAN, No INTEGER, Yes INTEGER)) results
    GROUP BY rollup(Churn)
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("""
    SELECT Churn,
           SUM("0") as "0", SUM("1") as "1", SUM("2") as "2", SUM("3") as "3",
           SUM("4") as "4", SUM("5") as "5", SUM("6") as "6", SUM("7") as "7",
           SUM("8") as "8", (CASE WHEN SUM("9") IS NULL THEN 0 ELSE SUM("9") END) as "9",
           SUM("0"+"1"+"2"+"3"+"4"+"5"+"6"+"7"+"8"+(CASE WHEN "9" IS NULL THEN 0 ELSE "9" END)) as "ALL"
    FROM (
        SELECT * FROM crosstab(
            'SELECT churn, customer_service_calls, COUNT(*)::int
             FROM telecom_churn GROUP BY churn, customer_service_calls ORDER BY 1,2
        ') AS (
            Churn BOOLEAN, "0" INTEGER, "1" INTEGER, "2" INTEGER, "3" INTEGER,
            "4" INTEGER, "5" INTEGER, "6" INTEGER, "7" INTEGER, "8" INTEGER, "9" INTEGER)
    ) results
    GROUP BY rollup(Churn)
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("""
    SELECT Churn, SUM("0") as "0", SUM("1") as "1", SUM("0"+"1") as "ALL"
    FROM (
        SELECT * FROM crosstab('
            SELECT churn, (CASE WHEN customer_service_calls > 3 THEN 1 ELSE 0 END) as many_service_calls, COUNT(*)::int
            FROM telecom_churn GROUP BY churn, many_service_calls ORDER BY 1,2
        ') AS (
            Churn BOOLEAN, "0" INTEGER, "1" INTEGER
        )
    ) results
    GROUP BY rollup(Churn)
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


cursor.execute("""
    SELECT Churn, SUM("0") as "0", SUM("1") as "1", SUM("0"+"1") as "ALL"
    FROM (
        SELECT * FROM crosstab('
            SELECT churn, (
                CASE
                    WHEN customer_service_calls > 3 AND international_plan LIKE $$Yes$$
                    THEN 1
                    ELSE 0
                END) as many_calls_and_plan, COUNT(*)::int
            FROM telecom_churn GROUP BY churn, many_calls_and_plan ORDER BY 1,2
        ') AS (
            Churn BOOLEAN, "0" INTEGER, "1" INTEGER
        )
    ) results
    GROUP BY rollup(Churn)
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))
