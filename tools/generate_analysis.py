import pandas as pd
import matplotlib.pyplot as plt
import json
import datetime
import os
import psycopg2
from pathlib import Path


if __name__ == "__main__":

    OUTPUT_DIR = Path("/app/output")
    os.makedirs(OUTPUT_DIR, exist_ok = True)

    #################################################
    # Connects to db
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="nyc_taxi_trips",
        user="user",
        password="password")
    cur = conn.cursor()


    #################################################
    # Item 1
    cur.execute("""
        SELECT
            AVG(trip_distance)
        FROM
            trip
        WHERE 
            passenger_count <= 2;
    """)
    avg_dist = cur.fetchone()[0]
    print(f"Item 1 - Average trip travel distance with passengers num <= 2: {avg_dist:.2f} km")


    #################################################
    # Item 2 
    top_vendors = pd.read_sql("""
        SELECT
            vendor_id,
            SUM(total_amount)
        FROM
            trip
        WHERE 
            passenger_count <= 2
        GROUP BY
            vendor_id
        ORDER BY
            SUM(total_amount) DESC
        LIMIT
            3;
    """, con = conn)

    labels = top_vendors["vendor_id"]
    sizes = top_vendors["sum"]
    explode = (0.05, 0.05, 0.05)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=45)
    ax1.axis('equal')
    plt.title("Top 3 vendors")
    output_path = OUTPUT_DIR / "top_vendors.svg"
    plt.savefig(output_path)
    plt.close()
    print(f"Item 2 - Plot saved in {output_path}")


    #################################################
    # Item 3
    months_total = pd.read_sql("""
        SELECT
            DATE_PART('month', pickup_datetime)::INTEGER as month,
            SUM(total_amount)
        FROM
            trip
        WHERE 
            payment_type = 'Cash'
        GROUP BY
            DATE_PART('month', pickup_datetime);
    """, con = conn)

    months_total.sort_values("month", inplace = True)
    months_total["pct"] = months_total["sum"] / months_total["sum"].sum()
    plt.bar(months_total["month"], months_total["pct"])
    plt.xticks(range(1, 13), range(1, 13))
    plt.xlabel("Month")
    plt.ylabel("Ratio")
    plt.title("Monthly distribution of cash paid trips")
    output_path = OUTPUT_DIR / "mohtly_distribution.svg"
    plt.savefig(output_path)
    plt.close()
    print(f"Item 3 - Plot saved in {output_path}")


    #################################################
    # Item 4
    tips = pd.read_sql("""
        SELECT
            COUNT(*),
            DATE_PART('month', MAX(pickup_datetime))::INTEGER as month,
            DATE_PART('day', MAX(pickup_datetime))::INTEGER as day
        FROM
            trip
        WHERE 
            (pickup_datetime >= '2012-10-01' AND pickup_datetime < '2013-01-01' AND tip_amount > 0)
        GROUP BY
            DATE_PART('doy', pickup_datetime);
    """, con = conn)
    dates = [datetime.datetime(2012, row.month, row.day) for row in tips.itertuples()]
    tips["date"] = dates
    tips.sort_values("date", inplace = True)
    plt.figure(figsize=(12, 6))
    plt.plot(tips["date"], tips["count"], "o-")
    plt.xlabel("Days")
    plt.ylabel("Tips count")
    plt.title("Tips count per day from 2012-10 to 2012-12")
    output_path = OUTPUT_DIR / "tips_per_day.svg"
    plt.savefig(output_path)
    plt.close()
    print(f"Item 4 - Plot saved in {output_path}")


    #################################################
    # Bonus Item 1
    cur.execute("""
        SELECT
            AVG(dropoff_datetime - pickup_datetime)
        FROM
            trip
        WHERE 
            DATE_PART('dow', pickup_datetime) IN (0, 6)
    """)
    avg_time = cur.fetchone()[0].total_seconds()
    print(f"Bonus Item 1 - Average trip time on Sat and Sun: {avg_time:.2f} s")


    #################################################
    # Bonus Item 2
    trips_2010 = pd.read_sql("""
        SELECT
            pickup_longitude,
            pickup_latitude,
            dropoff_longitude,
            dropoff_latitude
        FROM
            trip
        WHERE 
            (pickup_datetime >= '2010-01-01' AND dropoff_datetime < '2011-01-01')
            AND (RANDOM() < 0.01)
        LIMIT
            1000;   
    """, con = conn)

    plt.figure(figsize = (8, 7))
    plt.scatter(trips_2010["pickup_longitude"], trips_2010["pickup_latitude"], label = "pickup",s = 0.2)
    plt.scatter(trips_2010["dropoff_longitude"], trips_2010["dropoff_latitude"], label = "dropoff", s = 0.2)
    plt.ylim((40.65, 40.85))
    plt.xlim((-74.1, -73.8))
    plt.ylabel("Latitude")
    plt.xlabel("Longitude")
    plt.title("Pickups and dropoff points in 2010")
    plt.legend()
    plt.tight_layout()
    output_path = OUTPUT_DIR / "pickups_dropoffs.svg"
    plt.savefig(output_path)
    plt.close()
    print(f"Bonus Item 2 - Plot saved in {output_path}")


    #################################################
    # Disconnects from DB
    cur.close()
    conn.close()


    #################################################
    # Saves processed data
    answers = dict()
    answers["item_1"] = avg_dist
    answers["item_2"] = top_vendors.to_dict("records")
    answers["item_3"] = months_total[["month", "pct"]].to_dict("records")
    answers["item_4"] = tips[["month", "day", "count"]].to_dict("records")
    answers["bonus_item_1"] = avg_time
    answers["bonus_item_2"] = trips_2010.to_dict("list")
    with open(OUTPUT_DIR / "answers.json", "w") as f:
        f.write(json.dumps(answers))

    print("All analyzed!")
    print(f"Answers data can be found in {OUTPUT_DIR / 'answers.json'}")

