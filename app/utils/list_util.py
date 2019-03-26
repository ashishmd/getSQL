def get_values_from_query_set(query_set, key):
    result = []
    for row in query_set.iterator():
        result.append(getattr(row, key))
    return result
