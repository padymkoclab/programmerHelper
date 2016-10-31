BEGIN;
CREATE TABLE users_user (

    public_id SERIAL NOT NULL,
    private_id SERIAL NOT NULL,
    username varchar(40) UNIQUE NOT NULL,
    display_name varchar(40) UNIQUE NOT NULL,
    age integer NOT NULL,
    bio text,
    location varchar(100) DEFAULT 'Earth',
    salary numeric DEFAULT 0.0,
    gender varchar(10) DEFAULT NULL,

    PRIMARY KEY (public_id, private_id),
    CONSTRAINT unique_ids UNIQUE(public_id, private_id),
    CHECK (gender IN ('woman', 'man')),
    CHECK (salary < 100)
);

CREATE OR REPLACE FUNCTION make_lowercase_name()
RETURNS trigger as $make_lowercase_name$
    BEGIN
        NEW.username = LOWER(NEW.username);
        NEW.age = GREATEST(1, 2, 3, 4, NEW.age);
        NEW.bio = CASE WHEN NEW.bio IS NULL THEN 'not bio' END;
        RETURN NEW;
    END;
$make_lowercase_name$ LANGUAGE plpgsql;


CREATE TRIGGER lowercase_name
    BEFORE INSERT OR UPDATE ON users_user
    FOR EACH ROW
    EXECUTE PROCEDURE make_lowercase_name();

INSERT INTO users_user (username, age, display_name, gender, salary) VALUES ('Me', 22, 'My name', 'man', 99);
INSERT INTO users_user (username, age, display_name, gender) VALUES ('He', 22, 'His name', NULL);


SELECT * FROM users_user;
END;
