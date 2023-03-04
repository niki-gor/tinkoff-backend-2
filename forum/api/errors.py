from forum.api.models import Error

ErrUserNotFound = Error(detail='user not found')
ErrAlreadyFriends = Error(detail='already friends')