create database forum;

\c forum;

create table if not exists
    users (
        user_id serial primary key,
        name text,
        about text,
        age integer,
        email text,
        hashed_password text
    );

create table if not exists
    friends (
        from_id integer not null,
        to_id integer not null,
        unique (from_id, to_id)
    );