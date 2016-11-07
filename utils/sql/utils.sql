
/*
Display count records in each table on 'public' schema
*/

DO $$
DECLARE
    count_records int;
    r record;
BEGIN

    FOR r IN
        SELECT "table_name", "table_schema"
        FROM information_schema.tables
        WHERE "table_schema" = 'public'

    LOOP
        EXECUTE 'SELECT COUNT(*) FROM ' || quote_ident(r.table_schema) || '.' || quote_ident(r.table_name) INTO count_records;
        RAISE NOTICE '% %', quote_ident(r.table_name), count_records;
    END LOOP;

END $$;

/*
SELECT
    truncate_text(U."alias"),
    truncate_text(U."id"::text),
FROM "users_user" AS U

--------------------------------------------
"Варфоломей";"7a8acbdc-d";"7a8acbdc-d";3
"тов. Натал";"d5a25bb8-5";"d5a25bb8-5";5
--------------------------------------------

*/
CREATE OR REPLACE FUNCTION truncate_text(text) RETURNS varchar AS $$
    BEGIN
        RETURN LEFT(CAST($1 AS varchar), 10);
    END;
$$ LANGUAGE plpgsql;
