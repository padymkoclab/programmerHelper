BEGIN;


DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

-- CREATE EXTENSIONS (create extension is can only do for superuser
CREATE EXTENSION IF NOT EXISTS unaccent SCHEMA public;
CREATE EXTENSION IF NOT EXISTS pgtap SCHEMA public;

-- CREATE TABLES

CREATE TABLE "public"."users_level"(

    name varchar(20),
    description text,

    PRIMARY KEY (name)
);

CREATE TABLE "public"."users_user" (

    public_user_id SERIAL NOT NULL UNIQUE,
    private_user_id SERIAL NOT NULL UNIQUE,
    username varchar(40) UNIQUE NOT NULL,
    display_name varchar(40) UNIQUE NOT NULL,
    age integer NOT NULL,
    bio text,
    location varchar(100) DEFAULT 'Earth',
    salary numeric DEFAULT 0.0,
    gender varchar(10) DEFAULT NULL,
    level_name varchar(20) NOT NULL,

    PRIMARY KEY (public_user_id, private_user_id),
    CONSTRAINT unique_ids UNIQUE(public_user_id, private_user_id),
    CHECK (gender IN ('woman', 'man')),
    CHECK (salary < 100),
    FOREIGN KEY (level_name) REFERENCES "public"."users_level"
);

CREATE TABLE "public"."users_work"(

    work_id serial PRIMARY KEY,
    public_user_id integer NOT NULL,
    private_user_id integer NOT NULL,
    name varchar(50) NOT NULL,

    FOREIGN KEY (public_user_id, private_user_id) REFERENCES "public"."users_user",
    UNIQUE (public_user_id, private_user_id, name)

);


-- CREATE FUNCTIONS

CREATE FUNCTION public.capfirst("value" TEXT) RETURNS TEXT AS $capfirst$
    BEGIN
        RETURN UPPER(LEFT("value", 1)) || LOWER(SUBSTRING("value", 2));
    END;
$capfirst$ LANGUAGE plpgsql;

CREATE FUNCTION public.make_lowercase_name() RETURNS trigger AS $make_lowercase_name$
    BEGIN
        NEW.username = LOWER(NEW.username);
        NEW.age = GREATEST(1, 2, 3, 4, NEW.age);
        NEW.bio = CASE WHEN NEW.bio IS NULL THEN 'not bio' END;
        RETURN NEW;
    END;
$make_lowercase_name$ LANGUAGE plpgsql;

CREATE FUNCTION public.slugify("value" TEXT, "allow_unicode" BOOLEAN) RETURNS TEXT AS $slugify$
    WITH "normalized" AS (
        SELECT
            CASE
                WHEN "allow_unicode" = TRUE THEN "value"
                ELSE public.unaccent("value")
            END AS "value"
    ),
    "remove_chars" AS (
        SELECT regexp_replace("value", E'[^\\w\\s-]', '', 'gi') AS "value"
        FROM "normalized"
    ),
    "lower" AS (
        SELECT LOWER("value") AS "value"
        FROM "remove_chars"
    ),
    "trimmed" AS (
        SELECT TRIM("value") AS "value"
        FROM "lower"
    ),
    "hyphenated" AS (
        SELECT regexp_replace("value", E'[-\\s]+', '-', 'gi') AS "value"
        FROM "trimmed"
    )
    SELECT "value" FROM "hyphenated";
$slugify$ LANGUAGE SQL STRICT IMMUTABLE;

CREATE FUNCTION public.slugify(TEXT) RETURNS TEXT AS 'SELECT public.slugify($1, false)'
LANGUAGE SQL IMMUTABLE STRICT;

CREATE FUNCTION public.slugify_level_name() RETURNS trigger AS $slugify_level_name$
    BEGIN
        NEW.name = public.slugify(NEW.name);
        RETURN NEW;
    END;
$slugify_level_name$ LANGUAGE plpgsql;

-- -- CREATE TRIGGERS

CREATE TRIGGER lowercase_name
    BEFORE INSERT OR UPDATE ON "public"."users_user"
    FOR EACH ROW
    EXECUTE PROCEDURE public.make_lowercase_name();

CREATE TRIGGER slugify
    BEFORE INSERT OR UPDATE OF name ON "public"."users_level"
    FOR EACH ROW
    EXECUTE PROCEDURE public.slugify_level_name();

-- -- GET RANDOM OBJECT

SELECT * FROM "public"."users_user" ORDER BY RANDOM() LIMIT 1;
SELECT * FROM "public"."users_user" LIMIT 1 OFFSET FLOOR(RANDOM() * (SELECT COUNT(*) FROM "public"."users_user"));
SELECT "users_user"."username", "users_work"."name" FROM "public"."users_work" JOIN "public"."users_user" USING (public_user_id, private_user_id);
SELECT * FROM "public"."users_level";

END;
