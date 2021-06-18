CREATE TABLE IF NOT EXISTS "trip" (
    vendor_id               text,
    pickup_datetime         timestamp,
    dropoff_datetime        timestamp,
    passenger_count         integer,
    trip_distance           double precision,
    pickup_longitude        double precision,
    pickup_latitude         double precision,
    -- rate_code
    -- store_and_fwd_flag
    dropoff_longitude       double precision,
    dropoff_latitude        double precision,
    payment_type            text,
    fare_amount             double precision,
    surcharge               double precision,
    tip_amount              double precision,
    tolls_amount            double precision,
    total_amount            double precision
);

CREATE INDEX idx_trip ON trip(pickup_datetime);
