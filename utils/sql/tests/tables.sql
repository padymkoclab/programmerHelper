
\unset ECHO
\i test_setup.sql

SELECT plan(45);

SELECT has_table('public', 'users_user'::name);
SELECT has_table('public', 'users_level'::name);
SELECT has_table('public', 'users_work'::name);

SELECT has_column('users_user', 'public_user_id');
SELECT has_column('users_user', 'private_user_id');
SELECT has_column('users_user', 'username');
SELECT has_column('users_user', 'display_name');
SELECT has_column('users_user', 'age');
SELECT has_column('users_user', 'bio');
SELECT has_column('users_user', 'location');
SELECT has_column('users_user', 'salary');
SELECT has_column('users_user', 'gender');
SELECT has_column('users_user', 'level_name');

SELECT has_column('users_level', 'name');
SELECT has_column('users_level', 'description');

SELECT has_column('users_work', 'work_id');
SELECT has_column('users_work', 'public_user_id');
SELECT has_column('users_work', 'private_user_id');
SELECT has_column('users_work', 'name');

SELECT col_is_pk('users_work', 'work_id');
SELECT col_is_pk('users_level', 'name');
SELECT col_is_pk('users_user', ARRAY['public_user_id', 'private_user_id']);

SELECT col_not_null('users_user', 'username');
SELECT col_not_null('users_user', 'display_name');
SELECT col_not_null('users_user', 'age');
SELECT col_not_null('users_user', 'level_name');

SELECT col_not_null('users_work', 'public_user_id');
SELECT col_not_null('users_work', 'private_user_id');
SELECT col_not_null('users_work', 'name');

SELECT col_type_is('users_level', 'name', 'character varying(20)');
SELECT col_type_is('users_level', 'description', 'text');

SELECT col_type_is('users_user', 'public_user_id', 'integer');
SELECT col_type_is('users_user', 'private_user_id', 'integer');
SELECT col_type_is('users_user', 'username', 'character varying(40)');
SELECT col_type_is('users_user', 'display_name', 'character varying(40)');
SELECT col_type_is('users_user', 'age', 'integer');
SELECT col_type_is('users_user', 'bio', 'text');
SELECT col_type_is('users_user', 'location', 'character varying(100)');
SELECT col_type_is('users_user', 'salary', 'numeric');
SELECT col_type_is('users_user', 'gender', 'character varying(10)');
SELECT col_type_is('users_user', 'level_name', 'character varying(20)');

SELECT col_type_is('users_work', 'work_id', 'integer');
SELECT col_type_is('users_work', 'public_user_id', 'integer');
SELECT col_type_is('users_work', 'private_user_id', 'integer');
SELECT col_type_is('users_work', 'name', 'character varying(50)');

SELECT * FROM finish();

ROLLBACK;
