from app.utils.import_export import read_csv
from app.models import Tables
from app.models import Columns


FILE_PATH = "test_files/test.csv"
FILE_PATH_COLUMN = "test_files/column_test_import.csv"


# @todo : currently we are importing test file. Later we will implement upload option.
def import_tables():
    table_names = read_csv.read_table_names(FILE_PATH)
    for table in table_names:
        table_data = Tables(table_name=table["Table Name"], alias=table["Alias"])
        table_data.save()
    return "Import was success."

def import_columns():
    column_names = read_csv.read_column_names(FILE_PATH_COLUMN)
    for column in column_names:
        column_data = Columns(table_name=column["Table Name"], column_name=column["Column Namae"],is_primary =column[" Primary"],is_indexed =["Indexed"], foreign_key_column_name =["Foreign key Column"], foreign_key_table_name =["Foreign Key Table"])
        column_data.save()
    return "Import was success for columns."
