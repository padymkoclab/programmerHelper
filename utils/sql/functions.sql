

CREATE OR REPLACE FUNCTION public.CAPFIRST("value" TEXT) RETURNS TEXT AS $CAPFIRST$
    BEGIN
        RETURN UPPER(LEFT("value", 1)) || LOWER(SUBSTRING("value", 2));
    END;
$CAPFIRST$ LANGUAGE plpgsql;


/*
Usage: SELECT CAPITALIZE('sda dasd asd asd') --> 'Sda Dasd Asd Asd'
*/
CREATE OR REPLACE FUNCTION CAPITALIZE(a text) RETURNS text AS $$
    DECLARE
        i varchar;
        result varchar := '';
    BEGIN
        FOREACH i IN ARRAY STRING_TO_ARRAY(a, E' ')
        LOOP
            result := result || ' ' || CAPFIRST(i);
        END LOOP;
        RETURN result;
    END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION public.slugify("value" TEXT, "allow_unicode" BOOLEAN) RETURNS TEXT AS $slugify$
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
