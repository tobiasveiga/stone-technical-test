# Stone Technical Test

Technical test for data engineering manager role

## Requirements

This script should run on any Ubuntu machine (inlcuding from AWS) that has Docker installed.
To install docker on your machine, please visit [docker installation tutorial](https://docs.docker.com/engine/install/ubuntu/).

If docker is installed than clone this repository and move to the root directory of the project:
```
git clone https://github.com/tobiasveiga/stone-technical-test.git
cd stone-technical-test
```


## 1) Download data
The raw data should be located in `database/data`.
If neccessary you can download the data with the download script by running `./tools/download_data.sh`.

## 2) Setup
First start Postgres and Python container with `./tools/start_containers.sh`
To prepare everything, run the script `./tools/setup.sh`. This script will:
- add schemas to the DB
- install python requirements
- preprocess the  data
- feed the processed data to the DB

## 3) Analyze
Run the python script `tools/generate_analysis.py`:
```
docker exec -it py3 python tools/generate_analysis.py
```
or enter the container and run the script from there:
```
docker exec -it py3 /bin/bash
python tools/generate_analysis.py
```
Outputs of the analysis will be located in `output/`.

Storytelling `Analysis.html` file can be found in the root of this project. 

## Notes

### Programming choices
#### - Docker network configuration
Ideally I would use `--network host` configuration in both containers for faster perfomance but this in only available on Linux and I had only available a Windows machine to develop.

#### - Data preprocessing
The data preprocessing ignore two fields with null data ang normalize the payment_type field to speed up analysis later.

It also changes the JSON data to CSV data. I have chosen this because Postgres can copy CSV data very fast to the DB. This choice also makes sense because although data was in JSON format, it was clearly relational data (and I am supposed to use SQL in this task).

And in a different context, I would use a C script to convert that JSON files into CSV, but I used python because of the task requirements.

### Entering the docker containers

- Postgres container: `docker exec -it postgres /bin/bash`
- Python container: `docker exec -it py3 /bin/bash`





