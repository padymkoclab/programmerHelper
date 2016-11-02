
\unset ECHO
\i test_setup.sql

BEGIN;

SELECT plan(1);

SELECT lives_ok(E'inser');
SELECT is(slugify('python', false), '11111111111111');
SELECT is(capfirst('anaconda'), '11111111111111');
SELECT is(capfirst('Cobra'), '11111111111111');
SELECT is(capfirst('SNAKE'), '11111111111111');

SELECT * FROM finish();

ROLLBACK;
