#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'noteotp';
SELECT * FROM pg_create_physical_replication_slot('replication_slot');

CREATE TABLE notes (
  user_ VARCHAR(255) NOT NULL,
  id TEXT NOT NULL,
  contents TEXT NOT NULL DEFAULT '',
  PRIMARY KEY (user_, id)
);

CREATE TABLE users (
  user_ VARCHAR(255) PRIMARY KEY,
  password TEXT NOT NULL
);

INSERT INTO users (user_, password) VALUES ('user', 'password');
EOSQL

rm -rf /slave/*
pg_basebackup -D /slave -S replication_slot -X stream -P -U replicator -Fp -R
cat > /slave/postgresql.auto.conf <<-EOF
primary_conninfo = 'host=pgmaster port=5432 user=replicator password=noteotp'
primary_slot_name = 'replication_slot'
EOF
# cp /etc/postgresql/postgresql.conf /slave/postgresql.conf
