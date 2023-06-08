CREATE DATABASE IF NOT EXISTS appdb DEFAULT CHARSET utf8mb4;

USE appdb;

CREATE TABLE users(
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    username CHAR(64) NOT NULL,
    password CHAR(64) NOT NULL,
    token CHAR(64) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO users (username, password, token) VALUES ("admin", "NDkwYjk4NWUtMjBhZC00NGUzLWFhMzUt", "admin_ZmExNzNiN2EtNWUwNS00MzFkLWE1YzMt");
INSERT INTO users (username, password, token) VALUES ("test", "YzMxZDQ5NWMtYjFlMS00MjZiLWJmNGYt", "test_MGQ3OTY1N2YtZmM1Ny00NmU1LWJiZDgt");
