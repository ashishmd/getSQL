import csv


def read_file(file_path):
    table_names = []
    with open(file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            table_names.append(row[0])
        csvFile.close()
    return table_names
