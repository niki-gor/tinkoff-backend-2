-- name: create_friends<!
insert into
    friends(
        from_id, to_id
    )
select
    :from_id, :to_id
where 
    not exists(
        select
            1
        from
            friends
        where
            from_id = :to_id and to_id = :from_id
    )
returning
    1;


-- name: accept_friends<!
update
    friends
set
    accepted_at = :accepted_at
where
    from_id = :to_id and to_id = :from_id and accepted_at is null
returning
    1;


-- name: are_friends$
select
    1
from
    friends
where
    ((from_id = :first_id and to_id = :second_id) or (from_id = :second_id and to_id = :first_id)) 
    and accepted_at is not null;