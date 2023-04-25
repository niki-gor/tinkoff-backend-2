-- name: create_user<!
insert into
    users(
        name, about, age, email, hashed_password, last_login_at
    )
values
    (:name, :about, :age, :email, :hashed_password, :last_login_at)
returning
    user_id;


-- name: get_all_users
select
    user_id, name, about, age, email, last_login_at
from
    users;


-- name: get_user_by_id^
select
    user_id, name, about, age, email, hashed_password, last_login_at
from
    users
where
    user_id = :user_id;


-- name: update_user_by_id!
update
    users
set
    name     = :name,
    about    = :about,
    age      = :age,
    email    = :email,
    hashed_password = :hashed_password,
    last_login_at = :last_login_at
where
    user_id = :user_id;