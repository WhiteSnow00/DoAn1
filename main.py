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

book = Book()


def range_name(sheet_name, start_col, start_row, end_col, end_row):
    return f'{sheet_name}!{start_col}{start_row}:{end_col}{end_row}'


def find_book_by(field_type, field):
    if (not field_type or not field):
        print('Null field_type or field!')
        return
    pos = 0
    found = False
    delete_range = get_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.delete_col, book.start_row, book.delete_col, book.end_row)
    )
    delete_list = delete_range.get('values', [])
    type_col = book.start_col
    match field_type:
        case 'id':
            type_col = 'A'
            type_range = get_values(
                SPREADSHEET_ID,
                range_name(book.sheet_name, type_col, book.start_row, type_col, book.end_row)
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
                range_name(book.sheet_name, type_col, book.start_row, type_col, book.end_row)
            )
            type_list = type_range.get('values', [])
            while (pos < len(type_list)):
                if (str(type_list[pos][0]).find(field) != -1 and delete_list[pos][0] != '1'):
                    found = True
                    break
                pos += 1
    result = [found, pos]
    return result


def append_book(values):
    if (not values):
        print('Null values!')
        return
    id = values[0]
    find_result = find_book_by('id', id)
    if (find_result[0]):
        print('Id already exists!')
        return
    value_range = append_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.start_col, book.start_row, book.end_col, book.end_row),
        [values]
    )
    result = value_range.get('updates', [])
    # print(result)
    return result


def get_books():
    value_range = get_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.start_col, book.start_row, book.end_col, book.end_row)
    )
    result = value_range.get('values', [])
    # print(result)
    return result


def get_book_by_id(id):
    if (not id):
        return get_books()
    find_result = find_book_by('id', id)
    if (not find_result[0]):
        print('No id found.')
        return
    pos = find_result[1]
    value_range = get_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.start_col, pos + 2, book.end_col, pos + 2)
    )
    result = value_range.get('values', [])
    # print(result)
    return result


def get_books_by_name(name):
    if (not name):
        return get_books()
    find_result = find_book_by('name', name)
    if (not find_result[0]):
        print('No name found.')
        return
    pos = find_result[1]
    value_range = get_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.start_col, pos + 2, book.end_col, pos + 2)
    )
    result = value_range.get('values', [])
    # print(result)
    return result


def update_book(values):
    if (not values):
        print('Null values!')
        return
    id = values[0]
    find_result = find_book_by('id', id)
    if (not find_result[0]):
        print('No id found.')
        return
    pos = find_result[1]
    value_range = update_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.start_col, pos + 2, book.end_col, pos + 2),
        [values]
    )
    result = value_range
    # print(result)
    return result


def delete_book_by_id(id):
    if (not id):
        print('Null id!')
        return
    values = ['1']
    find_result = find_book_by('id', id)
    if (not find_result[0]):
        print('No id found.')
        return
    pos = find_result[1]
    value_range = update_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.delete_col, pos + 2, book.delete_col, pos + 2),
        [values]
    )
    result = value_range
    print(result)
    return result


if __name__ == '__main__':
    # get_books()
    get_book_by_id('10')
    # get_books_by_name('K')
    # append_book(['9', 'test', '3', '5', '2', '100', '2000', 'Tốt', '80000'])
    # update_book(['9', 'test', '1', '1', '1', '100', '2000', 'Tốt', '80000'])
    # delete_book_by_id('5')
