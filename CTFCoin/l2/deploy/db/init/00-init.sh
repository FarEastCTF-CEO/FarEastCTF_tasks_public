#!/bin/bash
set -euo pipefail

# This script runs only on the first initialization of the MySQL data directory.
# It creates tables and inserts demo data + flag.

FLAG_VALUE="${FLAG:-CTF{ctfcoin_sqli_blacklist_bypass}}"

mysql=( mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" --protocol=tcp )

# Wait for server to accept connections
for i in {1..60}; do
  if mysqladmin -uroot -p"${MYSQL_ROOT_PASSWORD}" ping --silent >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

"${mysql[@]}" "${MYSQL_DATABASE}" <<SQL
CREATE TABLE IF NOT EXISTS cryptocurrency (
  id INT AUTO_INCREMENT PRIMARY KEY,
  crypto_name VARCHAR(64) NOT NULL UNIQUE,
  crypto_price VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO cryptocurrency (crypto_name, crypto_price) VALUES
  ('Bitcoin',  '62500'),
  ('Ethereum', '3400'),
  ('Litecoin', '90'),
  ('Monero',   '160')
ON DUPLICATE KEY UPDATE crypto_price=VALUES(crypto_price);

CREATE TABLE IF NOT EXISTS bank_admin_info (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL,
  password VARCHAR(64) NOT NULL,
  flag VARCHAR(255) NOT NULL,
  UNIQUE KEY uniq_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO bank_admin_info (username, password, flag) VALUES
  ('admin', 'supersecret', '${FLAG_VALUE}')
ON DUPLICATE KEY UPDATE flag=VALUES(flag);
SQL
