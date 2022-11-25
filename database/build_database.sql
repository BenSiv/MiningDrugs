/*
Creating new database to store information from scraping https://www.drugs.com/ website.
*/

-- Initilizing database
CREATE DATABASE drugs;

USE drugs;

-- Initilizing tables
CREATE TABLE drugs (
    id int NOT NULL AUTO_INCREMENT,
    drug_name varchar(255),
    generic_name varchar(255),
    PRIMARY KEY (id)
);

CREATE TABLE related_drugs (
    id int NOT NULL AUTO_INCREMENT,
    drug_id int NOT NULL,
    related int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (drug_id) REFERENCES drugs(id),
    FOREIGN KEY (related) REFERENCES drugs(id)
);

CREATE TABLE side_effects (
    id int NOT NULL AUTO_INCREMENT,
    side_effect_name varchar(255),
    description varchar(255),
    PRIMARY KEY (id)
);

CREATE TABLE drug_side_effects (
    id int NOT NULL AUTO_INCREMENT,
    drug_id int NOT NULL,
    side_effect_id int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (drug_id) REFERENCES drugs(id),
    FOREIGN KEY (side_effect_id) REFERENCES side_effects(id)
);

CREATE TABLE medical_conditions (
    id int NOT NULL AUTO_INCREMENT,
    medical_condition_name varchar(255),
    description varchar(255),
    PRIMARY KEY (id)
);

CREATE TABLE drug_medical_conditions (
    id int NOT NULL AUTO_INCREMENT,
    drug_id int NOT NULL,
    medical_condition_id int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (drug_id) REFERENCES drugs(id),
    FOREIGN KEY (medical_condition_id) REFERENCES medical_conditions(id)
);

SHOW TABLES;