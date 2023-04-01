-- name: create_friends_table#
drop table if exists
    friends;
create table
    friends (
        from_id integer not null,
        to_id integer not null,
        unique (from_id, to_id)
    );

-- name: create_friends<!
insert into
    friends
values
    (:from_id, :to_id)
on conflict
    do nothing
returning
    1;

-- name: are_friends$
select
    count(*) = 2
from
    friends
where
    (from_id = :first_id and to_id = :second_id) or 
    (from_id = :second_id and to_id = :first_id);