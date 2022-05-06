def object_attrs_to_self(obj, slf):
    for attr in dir(obj):
        if attr[0].isalpha():
            setattr(slf, attr, getattr(obj, attr))
