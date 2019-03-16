from typing import Any

from app.utils.import_export import read_csv
from app.models import Tables
from app.models import Columns


a = "test_files/test.csv"
COLUMN_FILE_PATH = "test_files/column_test_import.csv"


# @todo : currently we are importing test file. Later we will implement upload option.
def import_tables():

    table_names = read_csv.read_table_names(a)
    for table in table_names:
        table_data = Tables(table_name=table["Table Name"], alias=table["Alias"])
        table_data.save()
    return "Import was success."

def import_columns():
    column_names = read_csv.read_table_names(COLUMN_FILE_PATH)
    without_foreign = [x for x in column_names if not x["foreign_key_table_name"]]
    with_foreign = [x for x in column_names if x["foreign_key_table_name"]]
    for row in without_foreign:
        ##table_id = for  Tables.table_name='tablename'Tables.object.raw(id )
        ##table_id = Tables.object.all(table_name='table_name').Tables.object.get(id)
        table_id = Tables.objects.get(table_name=row["table_name"]).id
        column_data = Columns(table_id=table_id, column_name=row["column_name"], is_primary=row["is_primary"], is_indexed=row["is_indexed"])
        column_data.save()


    for row in with_foreign:

        table_id = Tables.objects.get(table_name=row["table_name"]).id
        foreign_table_id = Columns.object.filter(foreign_key_table_name='table_name').Columns.object.get('table_id')
        foreign_col_id = Columns.object.filter(foreign_table_id='table_id').Columns.object.get('column_name')  # type: Any
        column_data = Columns(table_id=table_id, column_name=column["Column Name"],is_primary =column[" Primary"],is_indexed =["Indexed"], foreign_col_id=["Foreign key Column"], foreign_table_id=["Foreign Key Table"])
        column_data.save()
    return "Import was success for columns."
