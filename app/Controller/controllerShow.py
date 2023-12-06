from ..Modal.query import getTableQuery

def makeShow(id, request_form, default_list, table, default_list_keys, **column_dict):
    selected_list = []
    selected_columns = []

    for key, value in request_form.items():
        if value == 'on':
            selected_list.append(key)
            selected_columns.append(column_dict[key])

    selected_columns = [column_dict[id]] + selected_columns
    selected_list = [id] + selected_list

    if len(selected_list) > 1:
        context = getTableQuery(table, selected_list)	

    else:
        context = getTableQuery(table, default_list_keys)
        selected_columns = default_list

    return selected_columns, context