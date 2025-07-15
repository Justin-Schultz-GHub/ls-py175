def error_for_list_title(title, lists):
    if any(lst['title'] == title for lst in lists):
        return 'The title must be unique.'
    elif not 1 <= len(title) <= 100:
        return 'The title must be between 1 and 100 characters'
    else:
        return None

def find_list_by_id(list_id, lists):
    for lst in lists:
        if lst['id'] == list_id:
            return lst

    return None

def error_for_todo_item_name(todo):
    return (
            'Todo names must be between 1 and 100 characters'
            if not 1 <= len(todo) <= 100
            else None
            )