-- DB bootstrap for the CoinBuzz CTF challenge

CREATE DATABASE IF NOT EXISTS bank_db;
USE bank_db;

DROP TABLE IF EXISTS cryptocurrency;
CREATE TABLE cryptocurrency (
  id INT PRIMARY KEY AUTO_INCREMENT,
  crypto_name VARCHAR(32) UNIQUE,
  crypto_price INT
);

INSERT INTO cryptocurrency (crypto_name, crypto_price) VALUES
('Bitcoin', 100),
('Ethereum', 110),
('Litecoin', 120),
('Monero', 140),
('Dash', 900),
('Ton', 1000);

DROP TABLE IF EXISTS bank_admin_info;
CREATE TABLE bank_admin_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  admin_user VARCHAR(25),
  admin_password VARCHAR(32),
  description VARCHAR(100)
);

INSERT INTO bank_admin_info (admin_user, admin_password, description) VALUES
('admin', 'password', 'Администратор сайта CoinBuzz'),
('bank_adm', 'Super_P@4$w0rd', 'Администратор MySQL (смена пароля просрочена)');

-- Flag is stored in a separate database (requires cross-db query)
CREATE DATABASE IF NOT EXISTS customer_secret_data;
USE customer_secret_data;

DROP TABLE IF EXISTS secret_flag;
CREATE TABLE secret_flag (
  flag VARCHAR(64)
);

INSERT INTO secret_flag (flag) VALUES ('CTF{c01nbuzz_sql_inj_1n_like}');
