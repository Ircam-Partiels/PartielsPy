def valueToPtldocFormat(value):
    if type(value) == bool:
        value = int(value)
    if type(value) != str:
        value = str(value)
    return value
