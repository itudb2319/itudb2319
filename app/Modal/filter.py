def makeFilter(orderBy, getFunc, request_form, default_list, table, default_list_keys, page, **column_dict):
    selected_list = []
    selected_columns = []
    search = ""
    for key, value in request_form.items():
        if value == 'show':
            selected_list.append(key)
            selected_columns.append(column_dict[key])
        elif key == 'orderBy':
            orderBy = value
        
        elif key == 'search':
            search = value

        elif key == 'page':
            page = value

    if len(selected_list) > 0:
        context, length = getFunc(selected_list, orderBy, search, page)

    else:
        context, length = getFunc(default_list_keys, orderBy, search, page)
        selected_columns = default_list

    return selected_columns, context, orderBy, length, page