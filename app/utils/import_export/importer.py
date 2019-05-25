from app.utils import constants
from app.utils.import_export import read_csv
from app.models import Tables
from app.models import Columns
from app.models import Relations
from app.models import Path
from app.utils import list_util

TABLE_FILE_PATH = "test_files/test.csv"
COLUMN_FILE_PATH = "test_files/column_test_import.csv"
RELATION_FILE_PATH = "test_files/relation.csv"


# @todo : currently we are importing test file. Later we will implement upload option.
def import_tables():
    table_names = read_csv.read_table_names(TABLE_FILE_PATH)
    for table in table_names:
        table_data = Tables(table_name=table["Table Name"], alias=table["Alias"])
        table_data.save()
    return "Import was success."


def import_columns():
    column_names = read_csv.read_table_names(COLUMN_FILE_PATH)
    without_foreign = [x for x in column_names if not x["foreign_key_table_name"]]
    with_foreign = [x for x in column_names if x["foreign_key_table_name"]]
    for row in without_foreign:
        table_id = Tables.objects.get(table_name=row["table_name"]).id
        column_data = Columns(table_id=table_id, column_name=row["column_name"], is_primary=row["is_primary"], is_indexed=row["is_indexed"])
        column_data.save()
    for row in with_foreign:
        table_id = Tables.objects.get(table_name=row["table_name"]).id
        foreign_key_table_id = Tables.objects.get(table_name=row["foreign_key_table_name"]).id
        foreign_key_column_id = Columns.objects.get(column_name=row["foreign_key_column_name"], table_id=foreign_key_table_id).id
        column_data = Columns(table_id=table_id, column_name=row["column_name"], is_primary=row["is_primary"],
                              is_indexed=row["is_indexed"],foreign_key_table_id=foreign_key_table_id, foreign_key_column_id=foreign_key_column_id)

        column_data.save()
    return "Import was success for columns."


def import_relations():
    data = read_csv.read_table_names(RELATION_FILE_PATH)
    for row in data:
        table_1_id = Tables.objects.get(table_name=row["table_1"]).id
        table_2_id = Tables.objects.get(table_name=row["table_2"]).id
        relation = Relations(table_1_id=table_1_id, table_2_id=table_2_id, type=constants.TABLE_MAPPING[row["type"]])
        relation.save()
    return "Relation import was success."


relations = Relations.objects.all()
path_flow = []
paths = []


def create_path():
    global path_flow
    global paths
    tables = Tables.objects.all()
    result = list_util.get_values_from_query_set(tables, 'id')

    for source in result:
        for destination in result:
            if destination == source:
                continue
            print("\n\npath from ", source, " to ", destination)
            root = Tree()
            root.data = source
            visited_ids = [root.data]
            iterate_path(root, destination, visited_ids)

            # storing the path in DB
            if paths:
                # storing the paths in a sorted manner based on length.
                sorted_paths = sorted(paths, key=lambda path: len(path))
                path_row = Path(base_table_id=source, final_table_id=destination, is_direct=False, path=sorted_paths)
                path_row.save()

            # clearing path variable for next iteration
            paths = []

    return "Path created."


def iterate_path(root, destination, visited_ids):
    global path_flow
    global paths
    required_relations = relations.filter(table_1_id=root.data)
    child_ids = list_util.get_values_from_query_set(required_relations, 'table_2_id')
    for id in visited_ids:
        if id in child_ids:
            child_ids.remove(id)

    if len(child_ids) == 0:
        return

    for id in child_ids:
        child = Tree()
        child.parent = root
        child.data = id
        if id == destination:
            calculate_path(child)
            paths.append(path_flow)
            print(path_flow)
            path_flow = []
        else:
            visited_ids.append(child.data)
            iterate_path(child, destination, visited_ids)
            visited_ids.remove(child.data)


def calculate_path(root):
    global path_flow
    if root.parent is not None:
        calculate_path(root.parent)
    path_flow.append(root.data)


class Tree:
    def __init__(self):
        self.parent = None
        self.data = None

