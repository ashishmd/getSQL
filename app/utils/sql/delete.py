# @todo: here we can implement some checks before deleting the data.
def delete_data(query):
    from app.utils.sql import execute
    return execute.run_query(query)
