
\unset ECHO
\i test_setup.sql

SELECT plan(8);

SELECT ok(slugify('AAAAAAA') = 'aaaaaaa', 'Test function "slugify"');
SELECT ok(slugify('AaAaaaAa a A') = 'aaaaaaaa-a-a', 'Test function "slugify"');
SELECT ok(slugify('    A B c   ') = 'a-b-c', 'Test function "slugify"');
SELECT ok(slugify('До конца') = 'до-конца', 'Test function "slugify"');
SELECT ok(slugify('My homeland is my power.') = 'my-homeland-is-my-power', 'Test function "slugify"');

SELECT ok(capfirst('My homeland is my power.') = 'My homeland is my power.', 'Test function "capfirst"');
SELECT ok(capfirst('MY HOMELAND IS MY POWER.') = 'My homeland is my power.', 'Test function "capfirst"');
SELECT ok(capfirst('my homeland is my power.') = 'My homeland is my power.', 'Test function "capfirst"');

SELECT * FROM finish();

ROLLBACK;
