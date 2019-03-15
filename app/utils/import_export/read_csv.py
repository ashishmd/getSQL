import csv


def read_table_names(file_path):
    table_names = []
    with open(file_path, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for line in reader:
            table_names.append(line)
        csvFile.close()
    return table_names

def read_column_names(file_path_column):
    column_names =[]
    with open(file_path_column, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for line in reader:
            column_names.append(line)
        csvFile.close ()

    return column_names