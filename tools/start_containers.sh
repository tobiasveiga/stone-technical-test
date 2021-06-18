docker run -d -it \
    --name postgres \
    -p 5432:5432 \
    -p 8889:8889 \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=nyc_taxi_trips \
    -v $(pwd):/app \
    -w /app \
    postgres

docker run -d -it \
    --name py3 \
    --network container:postgres \
    -v $(pwd):/app \
    -w /app \
    python:3