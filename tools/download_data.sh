DATA_DIR=database/data
mkdir -p $DATA_DIR
wget -P $DATA_DIR https://s3.amazonaws.com/data-sprints-eng-test/data-payment_lookup-csv.csv
wget -P $DATA_DIR https://s3.amazonaws.com/data-sprints-eng-test/data-vendor_lookup-csv.csv
wget -P $DATA_DIR https://s3.amazonaws.com/data-sprints-eng-test/data-sample_data-nyctaxi-trips-2009-json_corrigido.json
wget -P $DATA_DIR https://s3.amazonaws.com/data-sprints-eng-test/data-sample_data-nyctaxi-trips-2011-json_corrigido.json
wget -P $DATA_DIR https://s3.amazonaws.com/data-sprints-eng-test/data-sample_data-nyctaxi-trips-2012-json_corrigido.json