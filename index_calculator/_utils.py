import warnings


def object_attrs_to_self(obj, slf):
    """Copy object attributes to new object."""
    for attr in dir(obj):
        if attr[0].isalpha():
            setattr(slf, attr, getattr(obj, attr))


def kwargs_to_self(kwargs, slf):
    """Write kwargs to new object."""
    for key, value in kwargs.items():
        if not hasattr(slf, key):
            setattr(slf, key, value)
        if getattr(slf, key) is None:
            setattr(slf, key, value)


def check_existance(attr_dict, slf):
    """Check existance of values."""
    for key, value in attr_dict.items():
        test = False
        if value is None:
            method = "raise"
            test = True
        if value == "N/A":
            method = "warn"
            test = True
        if test:
            if hasattr(slf, key):
                return getattr(slf, key)
            else:
                msg = f"No {key} is selected. '{key}=...'"
                if method == "raise":
                    raise ValueError(msg)
                elif method == "warn":
                    warnings.warn(msg)
                    return value
        else:
            return value
