create table
    users (
        user_id serial primary key,
        name text,
        about text,
        age integer,
        email text,
        hashed_password text,
        last_login_at text
    );

create table
    friends (
        from_id integer not null,
        to_id integer not null,
        accepted_at text,
        unique(from_id, to_id),
        foreign key (from_id) references users(user_id) on delete cascade,
        foreign key (to_id) references users(user_id) on delete cascade
    );