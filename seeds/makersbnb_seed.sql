-- First, we must delete (drop) all our tables
DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP TABLE IF EXISTS properties;
DROP SEQUENCE IF EXISTS properties_id_seq;
DROP TABLE IF EXISTS bookings;
DROP SEQUENCE IF EXISTS bookings_id_seq;

-- Then, we recreate them
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    phone INTEGER
);

CREATE SEQUENCE IF NOT EXISTS properties_id_seq;
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR(255),
    cost_per_night INTEGER,

    user_id INTEGER
    CONSTRAINT fk_user FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE SEQUENCE IF NOT EXISTS bookings_id_seq;
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    user_id INTEGER
    CONSTRAINT fk_user FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    property_id INTEGER
    CONSTRAINT fk_property FOREIGN KEY(property_id)
        REFERENCES properties(id)
        ON DELETE CASCADE
);

-- Finally, we add any records that are needed for the tests to run
INSERT INTO users (username, email, password, phone) VALUES ('Venera', 'venera@gmail.com', 'venera123', 07463648536);
INSERT INTO users (username, email, password, phone) VALUES ('Andre', 'andre@gmail.com', 'andre123', 07463228136);
INSERT INTO users (username, email, password, phone) VALUES ('Booker', 'booker@gmail.com', 'booker123', 01163228136);

INSERT INTO properties (name, description, cost_per_night, user_id) VALUES ('London', 'Castle', 200, 2);
INSERT INTO properties (name, description, cost_per_night, user_id) VALUES ('Paris', 'Chateau', 150, 2);
INSERT INTO properties (name, description, cost_per_night, user_id) VALUES ('Astana', 'Yurt', 450, 1);

INSERT INTO bookings (start_date, end_date, user_id, property_id) VALUES ('2024-05-04', '2024-05-04', 3, 2);
INSERT INTO bookings (start_date, end_date, user_id, property_id) VALUES ('2024-05-04', '2024-05-09', 3, 3);
INSERT INTO bookings (start_date, end_date, user_id, property_id) VALUES ('2024-05-10', '2024-06-10', 3, 3);






