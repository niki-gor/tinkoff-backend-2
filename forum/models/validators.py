def name_exists_not_too_long(v):
    if v is not None and not 1 <= len(v) <= 30:
        raise ValueError("invalid name length")
    return v


def about_not_too_long(v):
    if v is not None and not len(v) <= 120:
        raise ValueError("too much info about you")
    return v


def age_i_can_believe(v):
    if v is not None and not 1 <= v <= 120:
        raise ValueError("I don't believe you")
    return v


def good_password(v):
    if v is None:
        return v
    if len(v) < 8:
        raise ValueError("password is too short")
    validations = [str.isdigit, str.islower, str.isupper]
    if not all(any(is_char_type(c) for c in v) for is_char_type in validations):
        raise ValueError("password should contain lower, upper and digit characters")
    return v
