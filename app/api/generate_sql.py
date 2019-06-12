from app.models.table import Tables
from app.models.column import Columns
from app.models.path import Path
from app.models.relation import Relations
from app.utils import string_utils
from app.utils import list_util


def create_query(request_data):
    """
    variables used are:
        table_ids -> list of table ids which are present in the request. It will be used to get the path.
        select_data -> list of columns to be added in SELECT substring of query
        where_conditions -> params sent in request for where conditions
        validated_condition_data -> validated version of where_conditions
    :param request_data: JSONString in the request
    :return: final set of queries.
    """
    select_fields = request_data['select_fields']
    where_conditions = None
    where_condition_type = None
    custom_conditions = None

    if 'where_conditions' in request_data:
        where_conditions = request_data['where_conditions']['where_clauses']
        where_condition_type = validate_where_condition_type(request_data['where_conditions']['where_clause_type'])
        custom_conditions = request_data['where_conditions']['custom_conditions']

    table_ids = []  # initializing the array of table ids that are used in the query.
    select_data = []  # initializing array of values of select columns

    populate_select_data_and_table_ids(select_fields, select_data, table_ids)

    validated_condition_data = []  # initializing formatted value of where conditions.
    populate_validated_conditions_and_table_ids(where_conditions, validated_condition_data, table_ids)

    left_join_table_ids = []  # initializing list of table_ids that need to be left joined in query
    is_global_left_join = False
    if 'where_conditions' in request_data:
        is_global_left_join = request_data['where_conditions']['skip_data_presence_check']
        if not is_global_left_join:
            populate_left_join_table_ids(request_data, left_join_table_ids, table_ids)

    return build_query(select_data, table_ids, validated_condition_data, where_condition_type, custom_conditions, is_global_left_join, left_join_table_ids)


def validate_where_condition(condition, key, hash_data, table_ids):
    """
    @TODO: Need to throw error if condition column is wrong.
    This method is supposed to validate and throw error if condition value is wrong.
    Also we have a array of table_ids to keep track of all tables required to generate path.
        We will add value to it if a new table is found in condition
    :param condition:
    :param key: primary_value or secondary_value of condition
    :param hash_data: formatted / validated form of param - condition
    :param table_ids:
    :return: nil (we will be populating values in hash_data and table_ids)
    """
    value = condition[key]
    array = value.split(".")
    table_column, table_id = validate_and_get_table_column(array)
    if table_column:
        hash_data[key] = table_column
        list_util.append_to_list_with_check(table_id, table_ids)


def build_query(select_data, table_ids, where_conditions, where_condition_type, custom_conditions, is_global_left_join, left_join_table_ids):
    """
    This is the abstracted method where we build the query.
    We will build one query each for a path fetched.
    :param select_data:
    :param table_ids:
    :param where_conditions:
    :param where_condition_type: "AND" / "OR"
    :param custom_conditions: String for customized and/or case for where clauses.
    :param is_global_left_join: whether to use LEFT JOINS or not.
    :param left_join_table_ids: Tables for which we should use LEFT JOINS
    :return: list of queries
    """
    queries = []
    select_string = create_select_string(select_data)
    table_paths, table_strings = create_table_string(table_ids, is_global_left_join, left_join_table_ids)
    where_string = crete_where_string(where_conditions, where_condition_type, custom_conditions)

    if not table_paths:
        return select_string + table_strings + ";"
    for i in range(len(table_paths)):
        query = select_string + table_strings[i] + where_string + ";"
        hash_data = {'path': str(table_paths[i]).replace(',', ' -> '), 'query': query}
        queries.append(hash_data)
    return queries


def crete_where_string(where_conditions, where_condition_type, custom_conditions):
    """
    This method create the WHERE Condition substring of the query.
    Handled case where conditions can be in 2 format. It can have either quotes around it or not.
        Eg. Select ... WHERE a = 'abc'  ||   Select ... WHERE a = 123
    :param where_conditions: it is hash of validated where conditions.
    :param where_condition_type: "AND" / "OR"
    :param custom_conditions: String for customized and/or case for where clauses.
    :return: WHERE condition.
    """
    string = " WHERE "

    if where_condition_type == 'custom':
        for condition in where_conditions:
            primary_value = "\'" + condition['primary_value'] + "\'" if condition['primary_type'] == 'string' else condition['primary_value']
            secondary_value = "\'" + condition['secondary_value'] + "\'" if condition['secondary_type'] == 'string' else condition['secondary_value']
            where_string = "(" + primary_value + " " + condition['operator'] + " " + secondary_value + ")"
            custom_conditions = custom_conditions.replace("#" + str(condition['id']), where_string)
            custom_conditions = custom_conditions.replace(" and ", " AND ")
            custom_conditions = custom_conditions.replace(" or ", " OR ")
        return string + custom_conditions

    first = True
    for condition in where_conditions:
        primary_value = "\'" + condition['primary_value'] + "\'" if condition['primary_type'] == 'string' else condition['primary_value']
        secondary_value = "\'" + condition['secondary_value'] + "\'" if condition['secondary_type'] == 'string' else condition['secondary_value']
        if not first:
            string += where_condition_type
        string += "" + primary_value + " " + condition['operator'] + " " + secondary_value
        first = False
    return string


def create_select_string(select_data):
    string = "Select "
    delimiter = ", "
    string += delimiter.join(select_data)
    return string


def create_table_string(table_ids, is_global_left_join, left_join_table_ids):
    """
    If table_ids length is 1, it means, Query has only one table. SO query can be like below example:
        Eg: Select * from School where School.Name = 'ABC'
    If more table_ids are present, we need to iterate all possible paths that include those tables. One thing to note
        here is that both start and end of the path should be a table_id from the list.
    :param table_ids: list of tables to be included in query
    :param is_global_left_join: whether to use LEFT JOINS or not.
    :param left_join_table_ids: Tables for which we should use LEFT JOINS
    :return: FORM substring of the query
    """
    if len(table_ids) == 1:
        string = " FROM "
        string += Tables.objects.get(id=table_ids[0]).table_name
        return [[], string]
    else:
        required_path = []
        all_paths = Path.objects.filter(base_table_id__in=table_ids, final_table_id__in=table_ids)
        for path_row in all_paths:
            required_path += path_row.path
    required_paths = sorted([p for p in required_path if all(elem in p for elem in table_ids)],  key=lambda path: len(path))
    return create_query_string_from_path(required_paths, is_global_left_join, left_join_table_ids)


def create_query_string_from_path(paths, is_global_left_join, left_join_table_ids):
    """
    This method create FROM part of the query.
    There can be multiple valid paths for given conditions.
    Things to note.
        For has_one and has_many relations ships, foreign_key will be in secondary table
            Eg: School has_many Students. In this case Student table will have a school_id in it.
        For belongs_to case, foreign_key will be in primary table.
            Eg: Student belongs_to School. Then Student table will have a school_id in it.

    Variables Used:
        formatted_paths -> we will convert List of table_ids to List of table_names
        query_string_list -> we will have different version of FROM substring as per paths.
    :param paths: array of valid paths available
    :param is_global_left_join: whether to use LEFT JOINS or not.
    :param left_join_table_ids: Tables for which we should use LEFT JOINS
    :return: FormattedPaths and Substring of FROM conditions.
    """
    formatted_path_list = []
    query_string_list = []
    for path in paths:
        formatted_path = []
        query_string = [" FROM "]
        join_type = " INNER JOIN " if not is_global_left_join else " LEFT JOIN "
        is_join_type_set = False
        previous_table_id = None
        for table_id in path:
            if (not is_join_type_set) and (join_type == " INNER JOIN ") and (table_id in left_join_table_ids):
                join_type = " LEFT JOIN "
                is_join_type_set = True
            current_table_row = Tables.objects.get(id=table_id)
            formatted_path.append(current_table_row.table_name)
            if previous_table_id is not None:
                previous_table_row = Tables.objects.get(id=previous_table_id)
                relation_row = Relations.objects.get(table_1_id=previous_table_id, table_2_id=table_id)
                base_column = None
                final_column = None
                # @TODO: Currently relation type is hard coded below. We need to store it in the constants file and use it.
                if relation_row.type in [1, 2]:  # has_one and has_many
                    final_column = Columns.objects.get(table_id=table_id, foreign_key_table_id=previous_table_id)
                    base_column = Columns.objects.get(id=final_column.foreign_key_column_id)
                elif relation_row.type == 3:  # belongs_to
                    base_column = Columns.objects.get(table_id=previous_table_id, foreign_key_table_id=table_id)
                    final_column = Columns.objects.get(id=base_column.foreign_key_column_id)
                if base_column and final_column:
                    string = join_type + current_table_row.table_name + " ON " + previous_table_row.table_name + "." + \
                             base_column.column_name + " = " + current_table_row.table_name + "." + final_column.column_name
                    query_string.append(string)
                    previous_table_id = table_id
            else:
                query_string.append(" " + current_table_row.table_name)
                previous_table_id = table_id
        formatted_path_list.append(formatted_path)
        string_delimiter = " "
        table_string = string_delimiter.join(query_string)
        query_string_list.append(table_string)

    return [formatted_path_list, query_string_list]


def validate_and_get_table_column(array):
    """
    This method validates Column data passed in request params.
    @todo: Currently we are not throwing error if wrong data is passed. Need to work on it.
    :param array: array will have 2 values. First will be table name and second will be column name.
                Format will be -> [<table_name>, <column_name>]
    :return: array of column_name and table_id will be the return value.
                Format [<table.column_name>, table_id]
    """
    table_name, column_name = array

    table_row = Tables.objects.filter(alias=table_name).first()
    if table_row:
        table_id = table_row.id
        column_row = Columns.objects.filter(column_alias=column_name, table_id=table_id).first()
        if column_row:
            value = table_row.table_name + "." + column_row.column_name
            return [value, table_id]
        elif column_name == '*':
            value = table_row.table_name + "." + column_name
            return [value, table_id]
        else:
            raise ValueError('Invalid Column Name Passed: ' + column_name)
    else:
        raise ValueError('Invalid Table Name Passed: ' + table_name)
    return [None, None]


def validate_and_get_table_name(table_name):
    """
    This method validates Column data passed in request params.
    @todo: Currently we are not throwing error if wrong data is passed. Need to work on it.
    :param table_name: Camel case table name
    :return: table_id
    """
    table_row = Tables.objects.filter(alias=table_name).first()
    if table_row:
        return table_row.id
    raise ValueError('Invalid Table Name Passed: ' + table_name)


def validate_where_condition_type(condition_type):
    """
    @TODO: Ideally there should be a validator method to check all the API Params passed.
    Validates the condition_type passed in API request.
    :param condition_type:
    :return: by default returned value will be AND.
    """
    if not condition_type:
        return ' AND '
    if condition_type.lower() == 'and':
        return ' AND '
    elif condition_type.lower() == 'or':
        return ' OR '
    elif condition_type.lower() == 'custom':
        return condition_type.lower()
    return ' AND '


def validate_custom_conditions(condition_string):
    """
    @TODO: We should put a regex to check the condition sent in API like opening and closing braces etc.
    :param condition_string:
    :return:
    """
    return condition_string


def populate_select_data_and_table_ids(select_fields, select_data, table_ids):
    """
    This is a part of code which is moved to a method for better readability.
    This method will iterate select_fields from request and populate select_data.
    This method also populate table_ids list with tables used in select data.
    :param select_fields: param value from request
    :param select_data: validated and formatted list of select columns to be used in query
    :param table_ids: list of table_ids used in query
    :return: None
    """
    for field in select_fields:
        array = field.split(".")
        if len(array) == 2:
            table_column, table_id = validate_and_get_table_column(array)
            if table_column:
                list_util.append_to_list_with_check(table_column, select_data)
                list_util.append_to_list_with_check(table_id, table_ids)
        elif len(array) == 1:
            if array[0] == '*' and array[0] not in select_data:
                # Note: '*' should always be in the first position in the query.
                if not select_data:
                    select_data.append('*')
                else:
                    old_value = select_data[0]
                    select_data[0] = '*'
                    select_data.append(old_value)


def populate_validated_conditions_and_table_ids(where_conditions, validated_condition_data, table_ids):
    """
    This is a part of code which is moved to a method for better readability.
    This method will iterate where conditions, validate it and store it in a different hash.
    This method also populate table_ids list with tables used in where conditions.
    :param where_conditions: param value from request
    :param validated_condition_data: validated and formatted list of where clauses to be used in query.
    :param table_ids: list of table_ids used in query
    :return: None
    """
    if not where_conditions:
        return
    for condition in where_conditions:
        hash_data = {'primary_type': condition['primary_type'], 'operator': condition['operator'], 'id': condition['id']}
        for key in ['primary_type', 'secondary_type']:
            if condition[key] == 'column':
                value_key = 'primary_value' if key == 'primary_type' else 'secondary_value'
                validate_where_condition(condition, value_key, hash_data, table_ids)
            else:
                hash_data['secondary_value'] = condition['secondary_value']
                hash_data['secondary_type'] = condition['secondary_type']
        validated_condition_data.append(hash_data)


def populate_left_join_table_ids(request_data, left_join_table_ids, table_ids):
    """
    This is a part of code which is moved to a method for better readability.
    This method iterates tables given for left join, validates it and add its id to a list for later use.
    :param request_data: request param
    :param left_join_table_ids: list of tables that need to be left joined
    :param table_ids: list of table_ids used in query.
    :return: None
    """
    table_names = request_data['where_conditions']['skip_data_presence_tables']
    for table_name in table_names:
        table_id = validate_and_get_table_name(table_name)
        list_util.append_to_list_with_check(table_id, left_join_table_ids)
        list_util.append_to_list_with_check(table_id, table_ids)
