def convert_null_to_none(*args):
    """
    Convert `"null"` string to `None`
    """
    converted_args = []
    for arg in args:
        if arg == "null" or arg == "":
            converted_args.append(None)
        else:
            converted_args.append(arg)
    return tuple(converted_args)


def convert_to_python_bool(empty_string_default=True, *args):
    """
    Convert `"true"` string to `True` and `"false"` or `""` string to `False`
    """
    converted_args = []
    for arg in args:
        if arg == "true":
            converted_args.append(True)
        elif arg == "false":
            converted_args.append(False)
        else:
            converted_args.append(empty_string_default)
    return tuple(converted_args)
