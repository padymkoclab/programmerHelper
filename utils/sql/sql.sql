
-- CREATE EXTENSIONS (create extension is can only do for superuser
CREATE EXTENSION IF NOT EXISTS unaccent;

-- DROP TABLES

DROP TABLE IF EXISTS "users_level" CASCADE;
DROP TABLE IF EXISTS "users_user" CASCADE;
DROP TABLE IF EXISTS "users_work" CASCADE;

-- CREATE TABLES

CREATE TABLE IF NOT EXISTS users_level(
    name varchar(20),
    description text,
    PRIMARY KEY (name)
);


CREATE TABLE users_user (

    public_user_id SERIAL NOT NULL UNIQUE,
    private_user_id SERIAL NOT NULL UNIQUE,
    username varchar(40) UNIQUE NOT NULL,
    display_name varchar(40) UNIQUE NOT NULL,
    age integer NOT NULL,
    bio text,
    location varchar(100) DEFAULT 'Earth',
    salary numeric DEFAULT 0.0,
    gender varchar(10) DEFAULT NULL,
    level_name varchar(20),

    PRIMARY KEY (public_user_id, private_user_id),
    CONSTRAINT unique_ids UNIQUE(public_user_id, private_user_id),
    CHECK (gender IN ('woman', 'man')),
    CHECK (salary < 100),
    FOREIGN KEY (level_name) REFERENCES "users_level"
);

CREATE TABLE users_work(
    work_id serial PRIMARY KEY,
    public_user_id integer,
    private_user_id integer,
    name varchar(50),
    FOREIGN KEY (public_user_id, private_user_id) REFERENCES "users_user",
    UNIQUE (public_user_id, private_user_id, name)
);


-- CREATE FUNCTIONS

CREATE OR REPLACE FUNCTION make_lowercase_name()
RETURNS trigger AS $make_lowercase_name$
    BEGIN
        NEW.username = LOWER(NEW.username);
        NEW.age = GREATEST(1, 2, 3, 4, NEW.age);
        NEW.bio = CASE WHEN NEW.bio IS NULL THEN 'not bio' END;
        RETURN NEW;
    END;
$make_lowercase_name$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION slufigy_level_name("value" TEXT, "allow_unicode" BOOLEAN)
RETURNS TEXT AS $slufigy_level_name$
    WITH "normalized" AS (
        SELECT
            CASE
                WHEN "allow_unicode" = TRUE THEN "value"
                ELSE unaccent("value")
            END AS "value"
    ),
    "remove_chars" AS (
        SELECT LOWER("value") AS "value" FROM "normalized"
    )
    SELECT "value" FROM "remove_chars";
$slufigy_level_name$ LANGUAGE SQL STRICT IMMUTABLE;

-- CREATE TRIGGERS

CREATE TRIGGER lowercase_name
    BEFORE INSERT OR UPDATE ON users_user
    FOR EACH ROW
    EXECUTE PROCEDURE make_lowercase_name();

-- CREATE TRIGGER slufigy
--     BEFORE INSERT OR UPDATE ON users_level
--     FOR EACH ROW
--     EXECUTE PROCEDURE slufigy_level_name();


-- INSERT DATA

INSERT INTO users_level (name) VALUES ('REgular');
INSERT INTO users_level (name) VALUES ('Diamond-gold');
INSERT INTO users_level (name) VALUES ('Gold and silver');

INSERT INTO "users_user" (username, age, display_name, gender, salary, level_name)
    VALUES ('Me', 22, 'My name', 'man', 99, 'regular');
INSERT INTO "users_user" (username, age, display_name, gender, level_name)
    VALUES ('He', 22, 'His name', NULL, 'diamond-gold');
INSERT INTO "users_user" (username, age, display_name, gender, level_name)
    VALUES ('She', 22, 'Her name', NULL, 'gold-and-silver');

INSERT INTO  "users_work" (public_user_id, private_user_id, name)
    VALUES (1, 1, 'Pianino');
INSERT INTO  "users_work" (public_user_id, private_user_id, name)
    VALUES (2, 2, 'Roal');

-- GET RANDOM OBJECT
SELECT * FROM "users_user" ORDER BY RANDOM() LIMIT 1;
SELECT * FROM "users_user" LIMIT 1 OFFSET FLOOR(RANDOM() * (SELECT COUNT(*) FROM "users_user"));
SELECT "users_user"."username", "users_work"."name" FROM "users_work" JOIN "users_user" USING (public_user_id, private_user_id);
SELECT * FROM "users_level";
