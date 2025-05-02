CREATE DATABASE IF NOT EXISTS reservation_db;

\c reservation_db;


CREATE TABLE IF NOT EXISTS reservations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    salle_id INTEGER REFERENCES salles(id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL
);