from app.utils.sql import read, delete, execute


def delete_all_tables():
    query = "SELECT TABLE_NAME FROM information_schema.tables WHERE table_schema = 'get_sql'"
    data = read.get_data(query)
    query = "SET FOREIGN_KEY_CHECKS = 0"
    execute.run_query(query)
    status = True
    for table in data:
        query = "DROP TABLE IF EXISTS " + table.get("TABLE_NAME")
        status = delete.delete_data(query)
        if not status:
            break
    query = "SET FOREIGN_KEY_CHECKS = 1"
    execute.run_query(query)
    return status
