/*CREATE USER 'wexun'@'localhost' IDENTIFIED BY 'wexun';*/
DROP DATABASE IF EXISTS simhash;
CREATE DATABASE simhash;
GRANT ALL ON SIMHASH.* TO 'wexun'@'localhost';

USE SIMHASH;
CREATE TABLE item0
(
    item SMALLINT UNSIGNED,
    other VARCHAR(600),
    PRIMARY KEY(item)
);
CREATE TABLE item1
(
    item SMALLINT UNSIGNED,
    other VARCHAR(600),
    PRIMARY KEY(item)
);
CREATE TABLE item2
(
    item SMALLINT UNSIGNED,
    other VARCHAR(600),
    PRIMARY KEY(item)
);
CREATE TABLE item3
(
    item SMALLINT UNSIGNED,
    other VARCHAR(600),
    PRIMARY KEY(item)
);
