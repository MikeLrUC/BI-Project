CREATE DATABASE wine;
CREATE USER admin WITH ENCRYPTED PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE wine TO admin;
SET client_encoding TO 'UTF-8';
SET server_encoding TO 'UTF-8';

CREATE TABLE facts_rating (
	id		 BIGINT,
	rating	 FLOAT(8) NOT NULL,
	reviewer_id BIGINT NOT NULL,
	category_id BIGINT NOT NULL,
	winery_id	 BIGINT NOT NULL,
	region_id	 BIGINT NOT NULL,
	wine_id	 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE category (
	id	 BIGINT,
	name VARCHAR(512) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE wine (
	id		 BIGINT,
	name	 VARCHAR(512) NOT NULL,
	designation VARCHAR(512),
	alcohol	 FLOAT(8),
	price	 FLOAT(8),
	varietal	 VARCHAR(512),
	PRIMARY KEY(id)
);

CREATE TABLE winery (
	id	 BIGINT,
	name VARCHAR(512) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE reviewer (
	id	 BIGINT,
	name	 VARCHAR(512) NOT NULL,
	review VARCHAR(2048),
	PRIMARY KEY(id)
);

CREATE TABLE region (
	id	 BIGINT,
	name VARCHAR(512) NOT NULL,
	PRIMARY KEY(id)
);

ALTER TABLE facts_rating ADD CONSTRAINT facts_rating_fk1 FOREIGN KEY (reviewer_id) REFERENCES reviewer(id);
ALTER TABLE facts_rating ADD CONSTRAINT facts_rating_fk2 FOREIGN KEY (category_id) REFERENCES category(id);
ALTER TABLE facts_rating ADD CONSTRAINT facts_rating_fk3 FOREIGN KEY (winery_id) REFERENCES winery(id);
ALTER TABLE facts_rating ADD CONSTRAINT facts_rating_fk4 FOREIGN KEY (region_id) REFERENCES region(id);
ALTER TABLE facts_rating ADD CONSTRAINT facts_rating_fk5 FOREIGN KEY (wine_id) REFERENCES wine(id);
