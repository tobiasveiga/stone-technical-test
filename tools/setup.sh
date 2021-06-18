docker exec -it postgres psql -U user -d nyc_taxi_trips -f /app/database/V1__initial_schema.sql

docker exec -it py3 pip install -r requirements.txt

docker exec -it py3 python tools/preprocess.py

docker exec -it postgres psql -U user -d nyc_taxi_trips -c "COPY trip FROM '/app/database/data/csv_data.csv' WITH (FORMAT CSV);"
