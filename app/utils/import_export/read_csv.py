import csv


def read_table_names(file_path):
    table_names = []
    with open(file_path, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for line in reader:
            table_names.append(line)
        csvFile.close()
    return table_names
