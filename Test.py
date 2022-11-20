        global listbook
        dellist(tree)
        val = searchEntry.get()
        get_book_by_id(val)
        #result = findbook('int(val)')
        if len(result) == 0:
            tk.messagebox.showinfo(title='Hi', message='Không có sách như tìm kiếm')
        else:
            for i in range(0, len(result)):
                result = tuple(map(tuple, value_range.get('values', [])))
                tree.insert('', 'end', result)
        # cursor.close()
        # conn.close()
    except Exception as e:
        pass
    finally:
        searchEntry.delete(0,'end')