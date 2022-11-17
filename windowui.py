import tkinter as tk
from tkinter import *
from pymysql import *
from tkinter import messagebox


# Edit Reader
def editreader():

    def appendbook_button():
        try:
            eb = entry_bookname.get()
            ea = entry_author.get()
            ec = entry_company.get()
            ep = entry_place.get()
            connect_db = connect(host='localhost', port=3306, user='root', password='', database='library')
            cursor = conn.cursor()
            cursor.execute(
                'insert into students (stu_id, stu_name, stu_college, stu_class) values ("%s", "%s", "%s", "%s");'
                % (eb, ea, ec, ep))
            conn.commit()
            tk.messagebox.showinfo(title='Hi', message='Đã thêm người đọc thành công!')
        except Exception as e:
            pass
        finally:
            entry_bookname.delete('0', 'end')
            entry_author.delete('0', 'end')
            entry_company.delete('0', 'end')
            entry_place.delete('0', 'end')
            cursor.close()
            conn.close()

    def revisebook_button():
        try:
            eb = entry_bookname.get()
            ea = entry_author.get()
            ec = entry_company.get()
            ep = entry_place.get()
            conn = connect_db(host='localhost', port=3306, user='root', password='', database='library')
            cursor = conn.cursor()
            cursor.execute(
                'update students set stu_id="%s", stu_name="%s", stu_college="%s", stu_class="%s" where place="%s";'
                % (eb, ea, ec, ep, eb))
            conn.commit()
            tk.messagebox.showinfo(title='Hi', message='Reader modified successfully!')
        except Exception as e:
            pass
        finally:
            entry_bookname.delete('0', 'end')
            entry_author.delete('0', 'end')
            entry_company.delete('0', 'end')
            entry_place.delete('0', 'end')
            cursor.close()
            conn.close()

    editwindow = tk.Toplevel()
    editwindow.title('edit reader')
    editwindow.geometry('450x300+800+300')
    editwindow.resizable(0, 0)

    var = tk.StringVar()
    tk.Label(editwindow, text='student ID:').place(x=50, y=20)
    tk.Label(editwindow, text='Tên:').place(x=50, y=60)
    tk.Label(editwindow, text='Trường:').place(x=50, y=100)
    tk.Label(editwindow, text='Lớp:').place(x=50, y=140)

    val_eb = tk.StringVar()
    val_ea = tk.StringVar()
    val_ec = tk.StringVar()
    val_ep = tk.StringVar()

    entry_bookname = tk.Entry(editwindow, textvariable=val_eb)
    entry_author = tk.Entry(editwindow, textvariable=val_ea)
    entry_company = tk.Entry(editwindow, textvariable=val_ec)
    entry_place = tk.Entry(editwindow, textvariable=val_ep)

    entry_bookname.place(x=160, y=20)
    entry_author.place(x=160, y=60)
    entry_company.place(x=160, y=100)
    entry_place.place(x=160, y=140)

    btn_append = tk.Button(editwindow, text='Thêm người đọc', command=appendbook_button)
    btn_remove = tk.Button(editwindow, text='Modify readers', command=revisebook_button)
    btn_append.place(x=150, y=260)
    btn_remove.place(x=250, y=260)


# edit book
def editbook():

    def appendbook_button():
        try:
            ei = entry_book_id.get()
            eb = entry_book_name.get()
            ea = entry_book_author.get()
            ec = entry_category_id.get()
            ep = entry_publish_year.get()
            ebp = entry_book_place.get()
            es = entry_sumbook.get()
            el = entry_lendbook.get()
            conn = connect_db(host='localhost', port=3306, user='root', password='', database='library')
            cursor = conn.cursor()
            cursor.execute(
                'insert into book (book_id, book_name, book_author, category_id, publish_year, book_place, sumbook, lendbook) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");'
                % (ei, eb, ea, ec, ep, ebp, es, el))
            conn.commit()
            tk.messagebox.showinfo(title='Hi', message='Sách đã được thêm thành công!')
        except Exception as e:
            pass
        finally:
            entry_bookname.delete('0', 'end')
            entry_author.delete('0', 'end')
            entry_company.delete('0', 'end')
            entry_place.delete('0', 'end')
            entry_sumbook.delete('0', 'end')
            entry_lendbook.delete('0', 'end')
            cursor.close()
            conn.close()


    def revisebook_button():
        try:
            eb = entry_bookname.get()
            ea = entry_author.get()
            ec = entry_company.get()
            ep = entry_place.get()
            es = entry_sumbook.get()
            el = entry_lendbook.get()
            conn = connect_db(host='localhost', port=3306, user='root', password='', database='library')
            cursor = conn.cursor()
            cursor.execute(
                'insert into book (book_name, book_author, book_comp, book_id, sumbook, lendbook) values ("%s", "%s", "%s", "%s", "%s", "%s");'
                % (eb, ea, ec, ep, es, el, es))
            conn.commit()
            tk.messagebox.showinfo(title='Hi', message='Sách đã được sửa đổi thành công!')
        except Exception as e:
            pass
        finally:
            entry_bookname.delete('0', 'end')
            entry_author.delete('0', 'end')
            entry_company.delete('0', 'end')
            entry_place.delete('0', 'end')
            entry_sumbook.delete('0', 'end')
            entry_lendbook.delete('0', 'end')
            cursor.close()
            conn.close()
    
    editwindow = tk.Toplevel()
    editwindow.title('Chỉnh sửa sách')
    editwindow.geometry('450x300+800+300')
    editwindow.resizable(0, 0)


    var = tk.StringVar()
    tk.Label(editwindow, text='Tên sách:').place(x=50, y=20)
    tk.Label(editwindow, text='Tác giả:').place(x=50, y=60)
    tk.Label(editwindow, text='NXB:').place(x=50, y=100)
    tk.Label(editwindow, text='Mã:').place(x=50, y=140)
    tk.Label(editwindow, text='Mã sách:').place(x=50, y=180)
    tk.Label(editwindow, text='Số lượng:').place(x=50, y=220)

    val_eb = tk.StringVar()
    val_ea = tk.StringVar()
    val_ea.set("Chọn")
    val_ec = tk.StringVar()
    val_ec.set("Chọn")
    val_ep = tk.StringVar()
    val_es = tk.StringVar()
    val_es.set("Chọn")
    val_el = tk.StringVar()
    val_el.set("Chọn")
    
    entry_bookname = tk.Entry(editwindow, textvariable=val_eb)
    entry_author = OptionMenu(editwindow, val_ea,"C++", "Java","Python","JavaScript","Rust","GoLang")
    entry_company = OptionMenu(editwindow, val_ec,"C++", "Java","Python","JavaScript","Rust","GoLang")
    entry_place = tk.Entry(editwindow, textvariable=val_ep)
    entry_sumbook = OptionMenu(editwindow, val_es,"C++", "Java","Python","JavaScript","Rust","GoLang")
    entry_lendbook = OptionMenu(editwindow, val_el,"C++", "Java","Python","JavaScript","Rust","GoLang")

    entry_bookname.place(x=160, y=20)
    entry_author.place(x=160, y=60)
    entry_company.place(x=160, y=100)
    entry_place.place(x=160, y=140)
    entry_sumbook.place(x=160, y=180)
    entry_lendbook.place(x=160, y=220)

    btn_append = tk.Button(editwindow, text='Thêm sách', command=appendbook_button)
    btn_remove = tk.Button(editwindow, text='Sửa sách', command=revisebook_button)
    btn_append.place(x=150, y=260)
    btn_remove.place(x=250, y=260)
    

if __name__ == '__main__':
    editbook()
    editreader()