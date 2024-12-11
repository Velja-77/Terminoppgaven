CREATE DATABASE score;

USE score;

CREATE TABLE player (
    id int NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);