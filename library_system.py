import tkinter as tk
from tkinter import ttk
from pymysql import *
from windowui import *
import pickle
import xlrd
from tkinter import messagebox
import time


listbook = []
power = False

# Xác định xem quản trị viên đã đăng nhập chưa
def log(func):
    global power
    def wrapper(*args, **kw):
        if power is False:
            tk.messagebox.showerror(title='Error', message='You are not logged in and do not have administrator rights')
        else:
            return func(*args, **kw)
    return wrapper

def none(func):
    global power
    def wrapper(*args, **kw):
        if power is False:
            tk.messagebox.showerror(title='Error', message='Chức năng chưa làm')
        else:
            return func(*args, **kw)
    return wrapper

# Đăng nhập người dùng
def usr():

    def usr_login():  # Chức năng đăng nhập
        global power
        usr_name = var_usr_name.get()  # Get the username and password entered in Entry
        usr_pwd = var_usr_pwd.get()  # Assign username and password to usr_n and usr_p respectively

        try:  #xử lý lỗi
            with open('usrs_info.pickle', 'rb') as usr_file:  # Load usrs_info.pickle (the folder where user information is stored) into usr_file
                usrs_info = pickle.load(usr_file)  #  Load the usr_file file and store it in the variable usrs_info
        except FileNotFoundError:  # FileNotFoundError:Nếu tệp chưa được tạo
            with open('usrs_info.pickle', 'wb') as usr_file:  # Create usrs_info.pickle and load it into usr_file
                usrs_info = {'admin': 'admin'}
                pickle.dump(usrs_info, usr_file)  # Cut the contents of the dictionary usrs_info to usr_file

        if usr_name in usrs_info:  # Nếu tên người dùng được nhập trong hộp nhập liệu nằm trong từ điển usrs_info thư mục
            if usr_pwd == usrs_info[usr_name]:  # Nếu mật khẩu được nhập trong hộp nhập tương ứng với chỉ mục của usr_name trong từ điển users_info
                tk.messagebox.showinfo(title='Welcome', message='Quản lý' + usr_name + ' đăng nhập thành công')  # đăng nhập thành công
                power = True
                var1.set('Quản lý' + usr_name + ' đã đăng nhập')
                userwindow.destroy()
            else:  # nếu không tương thích
                tk.messagebox.showerror(message='Mật khẩu không chính xác, vui lòng nhập lại mật khẩu.')
        else:  # Nếu không có user_name tương ứng trong thư mục user_info từ điển
            is_sign_up = tk.messagebox.askyesno(title='Welcome',  # Yêu cầu bạn đăng ký bằng một cửa sổ bật lên
                                                message='Người dùng không tồn tại, có đăng ký hay không')
            if is_sign_up is True:
                usr_sign_up()
            else:
                pass

    @log
    def usr_sign_up():

        def sign_up():  # Registration function
            np = new_pwd.get()  # get() to the value entered in the Entry in the Toplevel window
            npf = new_pwd_confirm.get()
            nn = new_name.get()
            with open('usrs_info.pickle', 'rb') as usr_file:  # Open usrs_info.pickle as read-only
                exist_usr_info = pickle.load(usr_file)
                if np != npf:  # If it is judged that np and npf are not the same
                    tk.messagebox.showerror(title='Error',
                                            message='Mật khẩu không khớp nhau')
                elif nn in exist_usr_info:  # Nếu người dùng đã tồn tại
                    tk.messagebox.showerror(title='Error', message='Tên người dùng này đã được đăng ký')
                else:
                    exist_usr_info[nn] = np  # Store nn and np in the dictionary exist_usr_info
                    with open('usrs_info.pickle', 'wb') as usr_file:  # Write the key-value pair in the dictionary exist_usr_info into usrs_info.pickle
                        pickle.dump(exist_usr_info, usr_file)
                    tk.messagebox.showinfo('Welcome', 'Thêm người dùng thành công!')  # Prompt for successful registration
                    window_sign_up.destroy()  #Close the registration window
                    

        window_sign_up = tk.Toplevel(userwindow)  # Khởi tạo cửa sổ
        window_sign_up.geometry('350x200')
        window_sign_up.title('registration window')

        new_name = tk.StringVar()
        new_name.set('')
        tk.Label(window_sign_up, text='username:').place(x=10, y=10)
        entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
        entry_new_name.place(x=150, y=10)

        new_pwd = tk.StringVar()
        tk.Label(window_sign_up, text='password:').place(x=10, y=50)
        entry_new_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
        entry_new_pwd.place(x=150, y=50)

        new_pwd_confirm = tk.StringVar()
        tk.Label(window_sign_up, text='Confirm Password:').place(x=10, y=90)
        entry_new_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
        entry_new_pwd_confirm.place(x=150, y=90)

        btn_confirm_sign_up = tk.Button(window_sign_up,
                                        text='Thêm người dùng',
                                        command=sign_up)
        btn_confirm_sign_up.place(x=150, y=130)

    userwindow = tk.Toplevel()
    userwindow.title('Admin login')
    userwindow.geometry('450x300+450+300')
    userwindow.resizable(0, 0)

    tk.Label(userwindow, text='Please login \nQuản lý thư viện\nUNETI', font=('Arial', 20)).place(x=110, y=40)
    tk.Label(userwindow, text='username:').place(x=100, y=150)
    tk.Label(userwindow, text='password:').place(x=100, y=190)

    var_usr_name = tk.StringVar()
    # var_usr_name.set('exampel@python.com')  # Give username's Entry an initial value
    entry_usr_name = tk.Entry(userwindow, textvariable=var_usr_name)
    entry_usr_name.place(x=160, y=150)

    var_usr_pwd = tk.StringVar()
    entry_usr_pwd = tk.Entry(userwindow, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.place(x=160, y=190)

    btn_login = tk.Button(userwindow, text='Đăng nhập', command=usr_login)
    btn_login.place(x=140, y=230)
    btn_sign_up = tk.Button(userwindow, text='Đăng ký', command=usr_sign_up)
    btn_sign_up.place(x=240, y=230)


# Find books
def search_button():
    try:
        global listbook
        dellist(tree)
        val = searchEntry.get()
        conn = connect(host='localhost', user='root', password='', database='library')
        cursor = conn.cursor()
        if(val==''):
            cursor.execute("select * from book where book_name like '%s%%';" % val)
        else:
            cursor.execute("select * from book where book_name = '%s' or book_author like '%s' or book_id like '%s';" % (val, val, val))
        result = cursor.fetchall()
        if len(result) == 0:
            tk.messagebox.showinfo(title='Hi', message='Thư viện đang hết sách, lượn chỗ khác chơi')
        else:
            for i in range(len(result)):
                listbook = result[i][0:]
                tree.insert('', 'end', value=listbook)
        cursor.close()
        conn.close()
    except Exception as e:
        pass
    finally:
        searchEntry.delete(0,'end')

# Show Books
def allbook_button():
    try:
        global listbook
        dellist(tree)
        val = searchEntry.get()
        conn = connect(host='localhost', user='root', password='', database='library')
        cursor = conn.cursor()
        cursor.execute("select * from book where book_id like '%s%%';" % val)
        result = cursor.fetchall()
        for i in range(len(result)):
            listbook = result[i][0:]
            tree.insert('', 'end', value=listbook)
        cursor.close()
        conn.close()
    except Exception as e:
        pass
    finally:
        pass


# Lending books
@log
def lendbook_button():
    try:
        sql1 = 'begin;'
        sql2 = 'insert into borrow (s_id, s_name, b_id, b_name, borrow_date, return_date) values ("%s", "%s", "%s", "%s", curdate(), date_add(curdate(), interval 1 month));'
        sql3 = 'update students set returnbook = returnbook + 1 where stu_id = "%s" and returnbook < 10;'
        sql4 = 'update book set lendbook = lendbook - 1 where book_id = "%s" and lendbook > 0;'
        sql5 = 'commit;'
        s_id = stu_idEntry.get()
        s_name = stu_nameEntry.get()
        val_lb = lb.get('0', 'end')
        for i in range(len(val_lb)):
            b_id = val_lb[i][0]
            b_name = val_lb[i][1]
            conn = connect(host='localhost', user='root', password='', database='library')
            cursor = conn.cursor()
            cursor.execute('select returnbook from students where stu_id="%s";' % s_id)
            result_rb = cursor.fetchall()
            cursor.execute('select lendbook from book where book_id="%s";' % b_id)
            result_lb = cursor.fetchall()
            if int(result_rb[0][0]) > 9:
                tk.messagebox.showwarning(title='Thông Báo', message=('the student<%s> borrow limit has been reached!' % s_name))
            elif int(result_lb[0][0]) < 1:
                tk.messagebox.showwarning(title='Thông Báo', message=('the book《%s》is borrowed！' % b_name))
            else:
                cursor.execute(sql1)
                cursor.execute(sql2 % (s_id, s_name, b_id, b_name))
                cursor.execute(sql3 % s_id)
                cursor.execute(sql4 % b_id)
                cursor.execute(sql5)
                conn.commit()
                lb.delete('0', 'end')
                tk.messagebox.showinfo(title='Thông Báo', message=('books《%s》successfully loaned to students <%s>！' % (b_name, s_name)))
            cursor.close()
            conn.close()

            myFile = open('log.txt', 'a')
            myFile.write('[%s],books《%s》successfully loaned to students<%s>！\n' % (time.asctime(), b_name, s_name))
            myFile.close()
    except IntegrityError as e:
        sign_up_stu = tk.messagebox.askyesno(title='Thông Báo', message='Học sinh chưa có trong hệ thống, có muốn thêm không?')
        if sign_up_stu is True:
            editreader()
        else:
            pass
    except IndexError as e:
        sign_up_stu = tk.messagebox.askyesno(title='Thông Báo', message='Học sinh chưa có trong hệ thống, có muốn thêm không?')
        if sign_up_stu is True:
            editreader()
        else:
            pass
    finally:
        search_button()


# Return books 
@log
def returnbook_button():
    try:
        sql1 = 'begin;'
        sql2 = 'delete from borrow where s_id = "%s" and b_id = "%s";'
        sql3 = 'update students set returnbook = returnbook - 1 where stu_id = "%s";'
        sql4 = 'update book set lendbook = lendbook + 1 where book_id = "%s";'
        sql5 = 'commit;'
        s_id = stu_idEntry.get()
        s_name = stu_nameEntry.get()
        val_lb = lb.get('0', 'end')
        for i in range(len(val_lb)):
            b_id = val_lb[i][0]
            b_name = val_lb[i][1]
            conn = connect(host='localhost', port=3306, user='root', password='', database='library')
            cursor = conn.cursor()
            cursor.execute('select returnbook from students where stu_id="%s";' % s_id)
            result_rb = cursor.fetchall()
            cursor.execute('select lendbook from book where book_id="%s";' % b_id)
            result_lb = cursor.fetchall()
            cursor.execute(sql1)
            cursor.execute(sql2 % (s_id, b_id))
            cursor.execute(sql3 % s_id)
            cursor.execute(sql4 % b_id)
            cursor.execute(sql5)
            conn.commit()
            lb.delete('0', 'end')
        cursor.close()
        conn.close()
        myFile = open('log.txt', 'a')
        myFile.write('[%s],student<%s>Books on loan《%s》successfully returned！\n' % (time.asctime(), s_name, b_name))
        myFile.close()
        tk.messagebox.showinfo(title='Thông Báo', message='trả sách thành công')
    except IntegrityError as e:
        pass
    except IndexError as e:
        pass
    finally:
        search_button()


# Delete Books
@log
def removebook_button():
    sign_up_stu = tk.messagebox.askyesno(title='Thông Báo', message='Có muốn xóa sách không？')
    if sign_up_stu is True:
        val_lb = lb.get('0', 'end')
        for i in range(len(val_lb)):
            b_id = val_lb[i][0]
            b_name = val_lb[i][1]
            conn = connect(host='localhost', user='root', password='', database='library')
            cursor = conn.cursor()
            cursor.execute('delete from book where book_id="%s" and book_name="%s";' % (b_id, b_name))
            conn.commit()
            cursor.close()
            conn.close()
            lb.delete('0', 'end')
        tk.messagebox.showinfo(title='Thông Báo', message='Xóa sách thành công!')
        search_button()
    else:
        pass

# Import books
#@log
def importbook_button():

    def item_selected(event): # hàm lựa chọn sách trên bảng
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
    def add_book_to_db(): # hàm lựa chọn sách trên bảng rồi thêm vào db
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item.get("values")
            try:
                eb = record[0]
                ea = record[1]
                ec = record[2]
                ep = record[3]
                es = record[4]
                el = record[5]
                et = record[6]
                ek = record[7]
                conn = connect(host='localhost', user='root', password='', database='library')
                cursor = conn.cursor()
                cursor.execute(
                    'insert into book (book_id, book_name, book_author, category_id, publish_year, book_place, sumbook, lendbook) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");'
                    % (eb, ea, ec, ep, es, el,et,ek))
                conn.commit()
                tk.messagebox.showinfo(title='Hi', message='Thêm sách thành công！')
            except Exception as e:
                print(e)
            finally:
                pass
    
    # Tạo cửa sổ thêm sách
    importwindow = tk.Toplevel()
    importwindow.title('Thêm sách')
    importwindow.geometry('1250x800')
    importwindow.resizable(1, 0)
    tree = ttk.Treeview(importwindow, columns=['1', '2', '3', '4', '5', '6', '7', '8'], show='headings', height=90)
    tree.column('1', width=115, anchor='center')
    tree.column('2', width=130, anchor='center')
    tree.column('3', width=130, anchor='center')
    tree.column('4', width=130, anchor='center')
    tree.column('5', width=145, anchor='center')
    tree.column('6', width=145, anchor='center')
    tree.column('7', width=145, anchor='center')
    tree.column('8', width=145, anchor='center')
    tree.heading('1', text='Số sách')
    tree.heading('2', text='Tên sách')
    tree.heading('3', text='Tác giả')
    tree.heading('4', text='ID Thể Loại')
    tree.heading('5', text='Năm xuất bản')
    tree.heading('6', text='Vị trí giá sách')
    tree.heading('7', text='Tồn kho')
    tree.heading('8', text='Sl có thể mượn')
    tree.place(x=0, y=0, anchor='nw')

    # Đọc data từ file excel
    data = xlrd.open_workbook('book.xls')
    table = data.sheets()[0]
    for i in range(table.nrows-1):
        try:
            li_book = table.row_values(i+1)
            tree.insert('', 'end', value=(li_book[1],li_book[2],li_book[3],li_book[4],li_book[5],li_book[6],li_book[7],li_book[8]))
        except Exception as e:
            pass

    tree.bind('<<TreeviewSelect>>', item_selected)

    # nút xác nhận chọn sách để đưa vào db
    btn_select = tk.Button(importwindow, text='Nhập sách', command=add_book_to_db)
    btn_select.place(x=1100, y=100)

# edit book
@log
def editbook_button():
    editbook()

# edit reader
@log
def editreader_button():
    editreader()

# View treeview
@log
def treeviewClick(event):
    for item in tree.selection():
        item_text = tree.item(item, 'values')
        lb.insert('end', (item_text[0], item_text[1], item_text[2]))

def dellb():
    lb.delete('0', 'end')
    win.mainloop()

# clear treeview
def dellist(y):
    x = y.get_children()
    for item in x:
        y.delete(item)

# User login
def loginuser():
    usr()

# View Student Information
@log
def viewstudent():
    try:
        global listbook
        stuwindow = tk.Toplevel()
        stuwindow.title('Thông tin sinh viên mượn sách')
        stuwindow.geometry('600x300+450+300')
        stuwindow.resizable(0, 0)
        tree_stu = ttk.Treeview(stuwindow, columns=['1', '2', '3', '4', '5', '6'], show='headings', height=14)
        tree_stu.column('1', width=100, anchor='center')
        tree_stu.column('2', width=100, anchor='center')
        tree_stu.column('3', width=100, anchor='center')
        tree_stu.column('4', width=100, anchor='center')
        tree_stu.column('5', width=100, anchor='center')
        tree_stu.column('6', width=100, anchor='center')
        tree_stu.heading('1', text='Mã sinh viên')
        tree_stu.heading('2', text='Tên sinh viên')
        tree_stu.heading('3', text='Mã số sách')
        tree_stu.heading('4', text='Tên sách')
        tree_stu.heading('5', text='Ngày mượn')
        tree_stu.heading('6', text='Thời gian trả') #dự kiến

        tree_stu.place(x=0, y=0, anchor='nw')

        dellist(tree_stu)
        s_id = stu_idEntry.get()
        s_name = stu_nameEntry.get()
        conn = connect(host='localhost', port=3306, user='root', password='', database='library')
        cursor = conn.cursor()
        cursor.execute('select * from borrow where s_id = "%s" and s_name = "%s";' % (s_id, s_name))
        result = cursor.fetchall()
        for i in range(len(result)):
            listbook = result[i][1:]
            tree_stu.insert('', 'end', value=listbook)
        cursor.close()
        conn.close()
    except Exception as e:
        pass
    finally:
        pass

@log
def lend_book():

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
            tk.messagebox.showinfo(title='Thông Báo', message='Sách đã được cho mượn thành công!')
        except Exception as e:
            pass
        finally:
           ''' entry_bookname.delete('0', 'end')
            entry_author.delete('0', 'end')
            entry_company.delete('0', 'end')
            entry_place.delete('0', 'end')
            entry_sumbook.delete('0', 'end')
            entry_lendbook.delete('0', 'end')
            cursor.close()
            conn.close()'''
    
    editwindow = tk.Toplevel()
    editwindow.title('Mượn sách')
    editwindow.geometry('450x300+800+300')
    editwindow.resizable(0, 0)

    var = tk.StringVar()
    tk.Label(editwindow, text='Mã sv:').place(x=50, y=20)
    tk.Label(editwindow, text='Tên sv:').place(x=50, y=60)
    tk.Label(editwindow, text='Mã sách:').place(x=50, y=100)
    tk.Label(editwindow, text='Tên sách:').place(x=50, y=140)
    tk.Label(editwindow, text='Ngày mượn:').place(x=50, y=180)
    tk.Label(editwindow, text='Ngày trả:').place(x=50, y=220)

    val_eb = tk.StringVar()
    val_ea = tk.StringVar()
    val_ec = tk.StringVar()
    val_ep = tk.StringVar()
    val_es = tk.StringVar()
    val_el = tk.StringVar()
    
    entry_bookname = tk.Entry(editwindow, textvariable=val_eb)
    entry_author = tk.Entry(editwindow, textvariable=val_ea)
    entry_company = tk.Entry(editwindow, textvariable=val_ec)
    entry_place = tk.Entry(editwindow, textvariable=val_ep)
    entry_sumbook = tk.Entry(editwindow, textvariable=val_es)
    entry_lendbook = tk.Entry(editwindow, textvariable=val_el)

    entry_bookname.place(x=160, y=20)
    entry_author.place(x=160, y=60)
    entry_company.place(x=160, y=100)
    entry_place.place(x=160, y=140)
    entry_sumbook.place(x=160, y=180)
    entry_lendbook.place(x=160, y=220)

    btn_append = tk.Button(editwindow, text='Cho mượn', command=appendbook_button)
    btn_append.place(x=150, y=260)

# Xem sinh viên mượn quá hạn
@log
def overtime():
    try:
        global listbook
        stuwindow = tk.Toplevel()
        stuwindow.title('Thông tin sinh viên mượn sách')
        stuwindow.geometry('600x300+450+300')
        stuwindow.resizable(0, 0)
        tree_stu = ttk.Treeview(stuwindow, columns=['1', '2', '3', '4', '5', '6'], show='headings', height=14)
        tree_stu.column('1', width=100, anchor='center')
        tree_stu.column('2', width=100, anchor='center')
        tree_stu.column('3', width=100, anchor='center')
        tree_stu.column('4', width=100, anchor='center')
        tree_stu.column('5', width=100, anchor='center')
        tree_stu.column('6', width=100, anchor='center')
        tree_stu.heading('1', text='Mã sinh viên')
        tree_stu.heading('2', text='Tên sinh viên')
        tree_stu.heading('3', text='Mã số sách')
        tree_stu.heading('4', text='Tên sách')
        tree_stu.heading('5', text='Ngày mượn')
        tree_stu.heading('6', text='Thời gian trả') #dự kiến

        tree_stu.place(x=0, y=0, anchor='nw')

        dellist(tree_stu)
        conn = connect(host='localhost', port=3306, user='root', password='', database='library')
        cursor = conn.cursor()
        cursor.execute("select * from borrow where return_date < curdate();")
        result = cursor.fetchall()
        for i in range(len(result)):
            listbook = result[i][1:]
            tree_stu.insert('', 'end', value=listbook)
        cursor.close()
        conn.close()
    except Exception as e:
        pass
    finally:
        pass

def edit_place():
    def place_e():
        try:
            epl = entry_publisher.get()
            ei = entry_id.get()
            ead = entry_address.get()
            ep = entry_phone.get()
            conn = connect_db(host='localhost', port=3306, user='root', password='', database='library')
            cursor = conn.cursor()
            cursor.execute(
                'insert into book (book_id, book_name, book_author, category_id, publish_year, book_place, sumbook, lendbook) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");'
                % (epl, ei, ead, ep))
            conn.commit()
            tk.messagebox.showinfo(title='Thông Báo', message='Đã sửa đổi tác giả thành công!')
        except Exception as e:
            pass
        finally:
           ''' entry_bookname.delete('0', 'end')
            entry_author.delete('0', 'end')
            entry_company.delete('0', 'end')
            entry_place.delete('0', 'end')
            entry_sumbook.delete('0', 'end')
            entry_lendbook.delete('0', 'end')
            cursor.close()
            conn.close()'''
    
    editwindow = tk.Toplevel()
    editwindow.title('Nhà Xuất Bản')
    editwindow.geometry('350x220+800+300')
    editwindow.resizable(0, 0)

    var = tk.StringVar()
    tk.Label(editwindow, text='ID nxb:').place(x=50, y=20)
    tk.Label(editwindow, text='Tên nxb:').place(x=50, y=60)
    tk.Label(editwindow, text='Địa chỉ:').place(x=50, y=100)
    tk.Label(editwindow, text='Số DT:').place(x=50, y=140)

    val_ei = tk.StringVar()
    val_epl = tk.StringVar()
    val_ead = tk.StringVar()
    val_ep = tk.StringVar()

    entry_id = tk.Entry(editwindow, textvariable=val_ei)
    entry_publisher = tk.Entry(editwindow, textvariable=val_epl)
    entry_address = tk.Entry(editwindow, textvariable=val_ead)
    entry_phone = tk.Entry(editwindow, textvariable=val_ep)

    entry_publisher.place(x=160, y=20)
    entry_id.place(x=160, y=60)
    entry_address.place(x=160, y=100)
    entry_phone.place(x=160, y=140)

    btn_append = tk.Button(editwindow, text='Sửa đổi', command=place_e)
    btn_append.place(x=150, y=180)

def edit_author():
    def author_e():
        try:
            ei = entry_id.get()
            ea = entry_author.get()
            ed = entry_diploma.get()
            conn = connect_db(host='localhost', port=3306, user='root', password='', database='library')
            cursor = conn.cursor()
            cursor.execute(
                'insert into book (book_id, book_name, book_author, category_id, publish_year, book_place, sumbook, lendbook) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");'
                % (ei, ea, ed))
            conn.commit()
            tk.messagebox.showinfo(title='Thông Báo', message='Đã sửa đổi tác giả thành công!')
        except Exception as e:
            pass
        finally:
           ''' entry_bookname.delete('0', 'end')
            entry_author.delete('0', 'end')
            entry_company.delete('0', 'end')
            entry_place.delete('0', 'end')
            entry_sumbook.delete('0', 'end')
            entry_lendbook.delete('0', 'end')
            cursor.close()
            conn.close()'''
    
    editwindow = tk.Toplevel()
    editwindow.title('Tác giả')
    editwindow.geometry('350x200+800+300')
    editwindow.resizable(0, 0)

    var = tk.StringVar()
    tk.Label(editwindow, text='Tên Tác Giả:').place(x=50, y=20)
    tk.Label(editwindow, text='ID Tác Giả:').place(x=50, y=60)
    tk.Label(editwindow, text='Bằng Cấp:').place(x=50, y=100)

    val_ei = tk.StringVar()
    val_ea = tk.StringVar()
    val_ed = tk.StringVar()

    entry_author = tk.Entry(editwindow, textvariable=val_ei)
    entry_id = tk.Entry(editwindow, textvariable=val_ea)
    entry_diploma = tk.Entry(editwindow, textvariable=val_ed)

    entry_author.place(x=160, y=20)
    entry_id.place(x=160, y=60)
    entry_diploma.place(x=160, y=100)

    btn_append = tk.Button(editwindow, text='Sửa đổi', command=author_e)
    btn_append.place(x=150, y=160)

def edit_category():
    def category_e():
        try:
            ei = entry_id.get()
            ec = entry_category.get()
            conn = connect_db(host='localhost', port=3306, user='root', password='', database='library')
            cursor = conn.cursor()
            cursor.execute(
                'insert into book (book_id, book_name, book_author, category_id, publish_year, book_place, sumbook, lendbook) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");'
                % (ei, ec))
            conn.commit()
            tk.messagebox.showinfo(title='Thông Báo', message='Đã sửa đổi thể loại sách thành công!')
        except Exception as e:
            pass
        finally:
           ''' entry_bookname.delete('0', 'end')
            entry_author.delete('0', 'end')
            entry_company.delete('0', 'end')
            entry_place.delete('0', 'end')
            entry_sumbook.delete('0', 'end')
            entry_lendbook.delete('0', 'end')
            cursor.close()
            conn.close()'''
    
    editwindow = tk.Toplevel()
    editwindow.title('Thể loại')
    editwindow.geometry('350x200+800+300')
    editwindow.resizable(0, 0)

    var = tk.StringVar()
    tk.Label(editwindow, text='Tên Thể Loại:').place(x=50, y=20)
    tk.Label(editwindow, text='ID Thể Loại:').place(x=50, y=60)

    val_ec = tk.StringVar()
    val_ei = tk.StringVar()

    entry_category = tk.Entry(editwindow, textvariable=val_ec)
    entry_id = tk.Entry(editwindow, textvariable=val_ei)

    entry_category.place(x=160, y=20)
    entry_id.place(x=160, y=60)

    btn_append = tk.Button(editwindow, text='Sửa đổi', command=category_e)
    btn_append.place(x=150, y=160)

def edit_book_place():
    def book_place_e():
        try:
            ei = entry_id_bp.get()
            eb = entry_bp.get()
            ebn = entry_bpn.get()
            conn = connect_db(host='localhost', port=3306, user='root', password='', database='library')
            cursor = conn.cursor()
            cursor.execute(
                'insert into book (book_id, book_name, book_author, category_id, publish_year, book_place, sumbook, lendbook) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");'
                % ( ei, eb, ebn))
            conn.commit()
            tk.messagebox.showinfo(title='Thông Báo', message='Đã sửa đổi vị tri sách thành công!')
        except Exception as e:
            pass
        finally:
           ''' entry_bookname.delete('0', 'end')
            entry_author.delete('0', 'end')
            entry_company.delete('0', 'end')
            entry_place.delete('0', 'end')
            entry_sumbook.delete('0', 'end')
            entry_lendbook.delete('0', 'end')
            cursor.close()
            conn.close()'''
    
    editwindow = tk.Toplevel()
    editwindow.title('Vị Trí Sách')
    editwindow.geometry('350x200+800+300')
    editwindow.resizable(0, 0)

    var = tk.StringVar()
    tk.Label(editwindow, text='ID Vị trí:').place(x=50, y=20)
    tk.Label(editwindow, text='Tên Vị Trí GS:').place(x=50, y=60)
    tk.Label(editwindow, text='Tên Giá Sách:').place(x=50, y=100)

    val_ei = tk.StringVar()
    val_eb = tk.StringVar()
    val_ebn = tk.StringVar()

    entry_id_bp = tk.Entry(editwindow, textvariable=val_ei)
    entry_bp = tk.Entry(editwindow, textvariable=val_eb)
    entry_bpn = tk.Entry(editwindow, textvariable=val_ebn)

    entry_id_bp.place(x=160, y=20)
    entry_bp.place(x=160, y=60)
    entry_bpn.place(x=160, y=100)

    btn_append = tk.Button(editwindow, text='Sửa đổi', command=book_place_e)
    btn_append.place(x=150, y=160)

# View logs
@log
def book_log():
    myFile = open('log.txt', 'r')
    content = myFile.read()
    print(content)
    myFile.close()
    
@none
def empty():
    var1.set('Chức năng chưa làm')

@log
def overuser():
    global power
    power = False
    var1.set('Admin is not logged in')


window1 = tk.Tk()
window1.title('Hệ thống quản lý thư viện')
window1.geometry('1600x900')
window1.resizable(1, 0)

menubar = tk.Menu(window1)

filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Quản trị', menu=filemenu)
filemenu.add_command(label='Đăng nhập', command=loginuser)
filemenu.add_command(label='Đăng xuất', command=overuser)

filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Quản lý danh mục', menu=filemenu)
filemenu.add_command(label='Nhà xuất bản', command=edit_place)
filemenu.add_command(label='Tác giả', command=edit_author)
filemenu.add_command(label='Vị trí sách', command=edit_book_place)
filemenu.add_command(label='Thể loại sách', command=edit_category)

filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Quản lý thẻ', menu=filemenu)
filemenu.add_command(label='Làm thẻ thư viện', command=loginuser)
filemenu.add_command(label='Cấp lại thẻ', command=overuser)
filemenu.add_command(label='Tra cứu thẻ', command=overuser)

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Sửa', menu=editmenu)
# editmenu.add_command(label='edit_reader', command=editreader_button)
editmenu.add_command(label='Sửa sách', command=editbook_button)

notemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Log', menu=notemenu)
notemenu.add_command(label='Thống kê số lượt mượn sách', command=empty)
notemenu.add_command(label='Thống kê số lượng sách có thể cho mượn', command=empty)
notemenu.add_command(label='Xem danh sách mượn quá hạn', command=overtime)
notemenu.add_command(label='Xem log', command=book_log)


tree = ttk.Treeview(window1, columns=['1', '2', '3', '4', '5', '6', '7', '8'], show='headings', height=90)
tree.column('1', width=115, anchor='center')
tree.column('2', width=175, anchor='center')
tree.column('3', width=100, anchor='center')
tree.column('4', width=150, anchor='center')
tree.column('5', width=175, anchor='center')
tree.column('6', width=175, anchor='center')
tree.column('7', width=175, anchor='center')
tree.column('8', width=175, anchor='center')
tree.heading('1', text='Số sách')
tree.heading('2', text='Tên sách')
tree.heading('3', text='Tác giả')
tree.heading('4', text='ID Thể Loại')
tree.heading('5', text='Năm xuất bản')
tree.heading('6', text='Vị Trí')
tree.heading('7', text='Tồn kho')
tree.heading('8', text='Sl có thể mượn')

tree.bind('<Double-1>', treeviewClick)

var1 = tk.StringVar()
var1.set('Quản trị viên chưa đăng nhập')
var2 = tk.StringVar()
userLabel = tk.Label(window1, textvariable=var1, width=25, height=5)

searchEntry = tk.Entry(window1)

searchButton = tk.Button(window1, text='Tìm sách',
                         width=10, height=1, command=search_button)

lendbookButton = tk.Button(window1, text='Mượn sách',
                         width=10, height=1, command=lendbook_button)

returnbookButton = tk.Button(window1, text='Trả sách',
                         width=10, height=1, command=returnbook_button)

removebookButton = tk.Button(window1, text='Xóa sách',
                         width=10, height=1, command=removebook_button)

importbookButton = tk.Button(window1, text='Thêm sách',
                         width=10, height=1, command=importbook_button)

clearbookButton = tk.Button(window1, text='Làm mới',
                         width=10, height=1, command=dellb)

viewstudentButton = tk.Button(window1, text='In4 mượn',
                         width=10, height=1, command=viewstudent)

lb = tk.Listbox(window1, listvariable=var2, width=30)


tk.Label(window1, text='\t Mèo méo meo mèo meo',
         font=('Arial', 9)).place(x=0, y=460, anchor='nw')


userLabel.place(x=30, y=0, anchor='nw')
searchEntry.place(x=10, y=65, anchor='nw')
searchButton.place(x=155, y=60, anchor='nw')
lendbookButton.place(x=155, y=145, anchor='nw')
viewstudentButton.place(x=155, y=175, anchor='nw')
returnbookButton.place(x=155, y=200, anchor='nw')
lb.place(x=0, y=230, anchor='nw')
removebookButton.place(x=0, y=420, anchor='nw')
importbookButton.place(x=40, y=420, anchor='nw')
clearbookButton.place(x=120, y=420, anchor='nw')

tree.place(x=240, y=0, anchor='nw')

window1.config(menu=menubar)
window1.mainloop()
