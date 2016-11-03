
\unset ECHO
\i test_setup.sql

SELECT plan(16);

SELECT has_schema('public');

SELECT lives_ok('INSERT INTO "public"."users_level" (name) VALUES ($$REgular$$);');
SELECT throws_ok('INSERT INTO "public"."users_level" (name) VALUES ($$REGULAR$$);', 'duplicate key value violates unique constraint "users_level_pkey"', 'Unique slug name of level');
SELECT throws_ok('INSERT INTO "public"."users_level" (name) VALUES ($$regular$$);', 'duplicate key value violates unique constraint "users_level_pkey"', 'Unique slug name of level');
SELECT lives_ok('INSERT INTO "public"."users_level" (name) VALUES ($$Diamond-gold$$);');
SELECT throws_ok('INSERT INTO "public"."users_level" (name) VALUES ($$diamond-gold$$);', 'duplicate key value violates unique constraint "users_level_pkey"', 'Unique slug name of level');
SELECT lives_ok('INSERT INTO "public"."users_level" (name) VALUES ($$Gold and silver$$);');
SELECT throws_ok('INSERT INTO "public"."users_level" (name) VALUES ($$gold-and-silver$$);', 'duplicate key value violates unique constraint "users_level_pkey"', 'Unique slug name of level');

SELECT lives_ok('INSERT INTO "public"."users_user" (username, age, display_name, gender, level_name) VALUES ($$She$$, 22, $$Her name$$, NULL, $$gold-and-silver$$);');
SELECT lives_ok('INSERT INTO "public"."users_user" (username, age, display_name, gender, salary, level_name) VALUES ($$Me$$, 22, $$My name$$, $$man$$, 99, $$regular$$);');
SELECT lives_ok('INSERT INTO "public"."users_user" (username, age, display_name, gender, level_name) VALUES ($$He$$, 22, $$His name$$, NULL, $$diamond-gold$$);');

SELECT lives_ok('INSERT INTO  "public"."users_work" ("public_user_id", "private_user_id", "name") SELECT "users_user"."public_user_id", "users_user"."private_user_id", $$Pianino$$ FROM "public"."users_user" LIMIT 1;');
SELECT lives_ok('INSERT INTO  "public"."users_work" ("public_user_id", "private_user_id", "name") SELECT "users_user"."public_user_id", "users_user"."private_user_id", $$Roal$$ FROM "public"."users_user" LIMIT 1;');
SELECT throws_ok('INSERT INTO  "public"."users_work" ("public_user_id", "private_user_id", "name") SELECT "users_user"."public_user_id", "users_user"."private_user_id", $$Roal$$ FROM "public"."users_user" LIMIT 1;');

PREPARE username_select AS SELECT username FROM users_user;
SELECT results_eq('SELECT "users_user"."username" FROM "public"."users_user";', 'username_select');

PREPARE user_select AS SELECT level_name FROM users_user;
SELECT results_eq(
    'SELECT "users_user"."level_name", "users_user"."username" FROM "public"."users_user"',
    $$VALUES ('gold-and-silver'::varchar(50), 'she'::varchar(50)), ('regular'::varchar(50), 'me'::varchar(50)), ('diamond-gold'::varchar(50), 'he'::varchar(50)) $$
);

SELECT * FROM finish();

ROLLBACK;
