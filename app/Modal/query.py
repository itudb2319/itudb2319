from .database import db
from os.path import join

def getTableQuery(table, filtered_list):
    columns = ', '.join(map(str, filtered_list))
    data = db.executeQuery(f"SELECT {columns} FROM {table}")
    print(f"SELECT {columns} FROM {table}")
    return data