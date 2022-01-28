

def snake_case_dict_to_camel(object_to_change):
    changed = {}
    for key, value in object_to_change.items():
        changed[to_camel_case(key)] = value
    return changed


def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])