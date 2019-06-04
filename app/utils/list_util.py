def get_values_from_query_set(query_set, key):
    result = []
    for row in query_set.iterator():
        result.append(getattr(row, key))
    return result


def append_to_list_with_check(value, data_list):
    if value and value not in data_list:
        data_list.append(value)
