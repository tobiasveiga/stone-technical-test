import json
import csv
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="arg parser")
    DEFAULT_PATH = "/app/database/data"
    parser.add_argument("--input_dir",  type=str, default=DEFAULT_PATH, help="specify directory path containing raw data files")
    parser.add_argument("--output_dir", type=str, default=DEFAULT_PATH, help="specify directory path of output processed files")

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_args()
    INPUT_DIR  = Path(args.input_dir)
    OUTPUT_DIR = Path(args.output_dir)

    files = [
        'data-sample_data-nyctaxi-trips-2009-json_corrigido.json',
        'data-sample_data-nyctaxi-trips-2010-json_corrigido.json',
        'data-sample_data-nyctaxi-trips-2011-json_corrigido.json',
        'data-sample_data-nyctaxi-trips-2012-json_corrigido.json'
    ]

    print("Preprocessing started.")

    type_to_lookup = dict()
    with open(INPUT_DIR / "data-payment_lookup-csv.csv") as f:
        f.readline()
        f.readline() # skips first two line
        for line in f:
            key, value = line.strip().split(",")
            type_to_lookup[key] = value

    FIELDNAMES = [
        'vendor_id',
        'pickup_datetime',
        'dropoff_datetime',
        'passenger_count',
        'trip_distance',
        'pickup_longitude',
        'pickup_latitude',
        # 'rate_code',
        # 'store_and_fwd_flag',
        'dropoff_longitude',
        'dropoff_latitude',
        'payment_type',
        'fare_amount',
        'surcharge',
        'tip_amount',
        'tolls_amount',
        'total_amount'
    ]

    i = 0
    with open(OUTPUT_DIR / "sample.csv", "w", newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=FIELDNAMES, extrasaction = 'ignore')
        for file in files:
            if i == 3:
                break
            print(f" > {file}")
            file_path = INPUT_DIR / file
            with open(file_path) as in_file:
                for line in in_file:
                    if i == 3:
                        break
                    record = json.loads(line)
                    record["payment_type"] = type_to_lookup.get(record["payment_type"], "foo")
                    writer.writerow(record)
                    i += 1
    print("Preprocessing finished.")
