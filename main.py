from snippets.sheet_append_values import append_values
from snippets.sheet_get_values import get_values
from snippets.sheet_update_values import update_values

SPREADSHEET_ID = '1woHLQaJU4PKlurYx2cT0k89pXVCRQBN0Hwr1rxgAUQI'

class Book:
    sheet_name = 'Sach'
    start_col = 'A'
    end_col = 'I'
    delete_col = 'J'
    start_row = 2
    end_row = 1000

book = Book()


def range_name(sheet_name, start_col, start_row, end_col, end_row):
    return f'{sheet_name}!{start_col}{start_row}:{end_col}{end_row}'


def find_book_id(id):
    book = Book()
    id_range = get_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.start_col, book.start_row, book.start_col, book.end_row)
    )
    id_list = id_range.get('values', [])
    delete_range = get_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.delete_col, book.start_row, book.delete_col, book.end_row)
    )
    delete_list = delete_range.get('values', [])
    pos = 0
    found = False
    while (pos < len(id_list)):
        if (id == id_list[pos][0] and delete_list[pos][0] != '1'):
            found = True
            break
        pos += 1
    result = [found, pos]
    return result


def append_book(values):
    id = values[0]
    find_result = find_book_id(id)
    if (find_result[0]):
        print('Id already exists!')
        return
    book = Book()
    value_range = append_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.start_col, book.start_row, book.end_col, book.end_row),
        [values]
    )
    result = value_range.get('updates', [])
    print(result)
    return result


def get_books():
    book = Book()
    value_range = get_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.start_col, book.start_row, book.end_col, book.end_row)
    )
    result = value_range.get('values', [])
    print(result)
    return result


def get_book_by_id(id):
    find_result = find_book_id(id)
    if (not find_result[0]):
        print('No id found.')
        return
    pos = find_result[1]
    book = Book()
    value_range = get_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.start_col, pos + 2, book.end_col, pos + 2)
    )
    result = value_range.get('values', [])[0]
    print(result)
    return result

def update_book(values):
    id = values[0]
    find_result = find_book_id(id)
    if (not find_result[0]):
        print('No id found.')
        return
    pos = find_result[1]
    book = Book()
    value_range = update_values(
        SPREADSHEET_ID,
        range_name(book.sheet_name, book.start_col, pos + 2, book.end_col, pos + 2),
        [values]
    )
    result = value_range
    print(result)
    return result


def delete_book_by_id(id):
    values = ['1']
    find_result = find_book_id(id)
    if (not find_result[0]):
        print('No id found.')
        return
    pos = find_result[1]
    book = Book()
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
    # get_book_by_id('5')
    # append_book(['9', 'test', '3', '5', '2', '100', '2000', 'Tốt', '80000'])
    # update_book(['9', 'test', '1', '1', '1', '100', '2000', 'Tốt', '80000'])
    delete_book_by_id('3')