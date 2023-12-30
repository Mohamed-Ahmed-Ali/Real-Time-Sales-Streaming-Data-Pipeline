#!/bin/bash

# Function to check ClickHouse availability
check_clickhouse() {
    until printf "" 2>>/dev/null >>/dev/tcp/clickhouse/9000; do
        sleep 5;
        echo "Waiting for ClickHouse...";
    done
}

# Wait for ClickHouse availability
check_clickhouse

echo "Creating database and table..."
clickhouse-client --host clickhouse --query "CREATE DATABASE IF NOT EXISTS order_db;"

clickhouse-client --host clickhouse --query "
CREATE TABLE IF NOT EXISTS order_db.order_table (
    uuid UUID,
    customer_id Int32,
    source String,
    quantity Int32,
    total Float32,
    created_at DateTime
) ENGINE = MergeTree()
ORDER BY (uuid);"
