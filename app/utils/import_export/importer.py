from app.utils.import_export import read_csv
from app.models import Tables


FILE_PATH = "test_files/test.csv"


def import_tables():
    table_names = read_csv.read_table_names(FILE_PATH)

    for table in table_names:
        table_data = Tables(table_name=table["Table Name"], alias=table["Alias"])
        table_data.save()
    return "Import was success."
