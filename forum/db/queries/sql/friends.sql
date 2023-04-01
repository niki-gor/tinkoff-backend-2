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