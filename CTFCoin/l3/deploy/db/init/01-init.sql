CREATE DATABASE IF NOT EXISTS bank_db;
USE bank_db;

DROP TABLE IF EXISTS cryptocurrency;
CREATE TABLE cryptocurrency (
  id INT AUTO_INCREMENT PRIMARY KEY,
  crypto_name VARCHAR(64) NOT NULL UNIQUE,
  crypto_price VARCHAR(64) NOT NULL
);

INSERT INTO cryptocurrency (crypto_name, crypto_price) VALUES
('Bitcoin', '68000'),
('Ethereum', '3500'),
('Litecoin', '85'),
('Monero', '160');

DROP TABLE IF EXISTS bank_admin_info;
CREATE TABLE bank_admin_info (
  id INT AUTO_INCREMENT PRIMARY KEY,
  flag VARCHAR(255) NOT NULL
);

INSERT INTO bank_admin_info (flag) VALUES
('FECTF{ctfcoin_sqli_blacklist_bypass}');
