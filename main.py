from snippets.sheet_append_values import append_values
from snippets.sheet_get_values import get_values
from snippets.sheet_update_values import update_values

SPREADSHEET_ID = '1woHLQaJU4PKlurYx2cT0k89pXVCRQBN0Hwr1rxgAUQI'

class Book:
    sheet_name = 'Sach'
    start_col = 'A'
    end_col = 'J'
    delete_col = 'K'
    start_row = 2
    end_row = 1000

class LibraryCard:
    sheet_name = 'TheThuVien'
    start_col = 'A'
    end_col = 'J'
    delete_col = 'K'
    start_row = 2
    end_row = 1000

book = Book()
lc = LibraryCard()


def range_name(sheet_name, start_col, start_row, end_col, end_row):
    return f'{sheet_name}!{start_col}{start_row}:{end_col}{end_row}'


def parse_object_name(object_name):
    match object_name:
        case 'book':
            return book
        case 'lc':
            return lc
        case _:
            print('object_name invalid!')
            return None


def find_object_by(object_name, field_type, field):
    object = parse_object_name(object_name)
    if (object == None):
        return [False, 0]
    if (not field_type or not field):
        print('Null field_type or field!')
        return [False, 0]
    pos = 0
    found = False
    delete_range = get_values(
        SPREADSHEET_ID,
        range_name(object.sheet_name, object.delete_col, object.start_row, object.delete_col, object.end_row)
    )
    delete_list = delete_range.get('values', [])
    type_col = object.start_col
    match field_type:
        case 'id':
            type_col = 'A'
            type_range = get_values(
                SPREADSHEET_ID,
                range_name(object.sheet_name, type_col, object.start_row, type_col, object.end_row)
            )
            type_list = type_range.get('values', [])
            while (pos < len(type_list)):
                if (field == type_list[pos][0] and delete_list[pos][0] != '1'):
                    found = True
                    break
                pos += 1
        case 'name':
            type_col = 'B'
            type_range = get_values(
                SPREADSHEET_ID,
                range_name(object.sheet_name, type_col, object.start_row, type_col, object.end_row)
            )
            type_list = type_range.get('values', [])
            while (pos < len(type_list)):
                if (str(type_list[pos][0]).find(field) != -1 and delete_list[pos][0] != '1'):
                    found = True
                    break
                pos += 1
    result = [found, pos]
    return result


def append_object(object_name, values):
    object = parse_object_name(object_name)
    if (object == None):
        return False
    if (not values):
        print('Null values!')
        return False
    id = values[0]
    values.append('0')
    find_result = find_object_by(object_name, 'id', id)
    if (find_result[0]):
        print('Id already exists!')
        return False
    value_range = append_values(
        SPREADSHEET_ID,
        range_name(object.sheet_name, object.start_col, object.start_row, object.delete_col, object.end_row),
        [values]
    )
    result = value_range.get('updates', [])
    # print(result)
    return result


def get_objects(object_name):
    object = parse_object_name(object_name)
    if (object == None):
        return False
    value_range = get_values(
        SPREADSHEET_ID,
        range_name(object.sheet_name, object.start_col, object.start_row, object.end_col, object.end_row)
    )
    result = value_range.get('values', [])
    # print(result)
    return result


def get_object_by_id(object_name, id):
    object = parse_object_name(object_name)
    if (object == None):
        return False
    if (not id):
        return get_objects(object_name)
    find_result = find_object_by(object_name, 'id', id)
    if (not find_result[0]):
        print('No id found.')
        return False
    pos = find_result[1]
    value_range = get_values(
        SPREADSHEET_ID,
        range_name(object.sheet_name, object.start_col, pos + 2, object.end_col, pos + 2)
    )
    result = value_range.get('values', [])
    # print(result)
    return result


def get_objects_by_name(object_name, name):
    object = parse_object_name(object_name)
    if (object == None):
        return False
    if (not name):
        return get_objects(object_name)
    find_result = find_object_by(object_name, 'name', name)
    if (not find_result[0]):
        print('No name found.')
        return False
    pos = find_result[1]
    value_range = get_values(
        SPREADSHEET_ID,
        range_name(object.sheet_name, object.start_col, pos + 2, object.end_col, pos + 2)
    )
    result = value_range.get('values', [])
    # print(result)
    return result


def update_object(object_name, values):
    object = parse_object_name(object_name)
    if (object == None):
        return False
    if (not values):
        print('Null values!')
        return False
    id = values[0]
    find_result = find_object_by(object_name, 'id', id)
    if (not find_result[0]):
        print('No id found.')
        return False
    pos = find_result[1]
    value_range = update_values(
        SPREADSHEET_ID,
        range_name(object.sheet_name, object.start_col, pos + 2, object.end_col, pos + 2),
        [values]
    )
    result = value_range
    # print(result)
    return result


def delete_object_by_id(object_name, id):
    object = parse_object_name(object_name)
    if (object == None):
        return False
    if (not id):
        print('Null id!')
        return False
    values = ['1']
    find_result = find_object_by(object_name, 'id', id)
    if (not find_result[0]):
        print('No id found.')
        return False
    pos = find_result[1]
    value_range = update_values(
        SPREADSHEET_ID,
        range_name(object.sheet_name, object.delete_col, pos + 2, object.delete_col, pos + 2),
        [values]
    )
    result = value_range
    print(result)
    return result


if __name__ == '__main__':
    object_name = 'lc'
    print(get_objects(object_name))
    # get_object_by_id(object_name, '10')
    # get_objects_by_name(object_name, 'K')
    # append_object(object_name, ['12', 'test', '3', '5', '2', '100', '2000', '10', '10', '80000'])
    # update_object(object_name, ['9', 'test', '1', '1', '1', '100', '2000', '10', '10', '80000'])
    # delete_object_by_id(object_name, '5')
