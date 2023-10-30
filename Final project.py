import tkinter as tk   # импортируем библиотеку tkinter
from tkinter import ttk   # импортируем модуль для отображения табличных данных
import sqlite3   # импортируем библиотеку базы данных

# создаем класс основного окна
class Main(tk.Frame):
    # создаем метод инициализации класса
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        # добавляем атрибут db
        self.db = db
        # добавляем метод для вывод данных в виджет
        self.view_records()


    # создаем метод для хранения и инициализации объектов GUI основного окна
    def init_main(self):
        # создание панели виджетов
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # создание кнопку добавления
        self.img_add=tk.PhotoImage(file='img/add.png') # добавляем иконку
        # встраивание в картинку кнопку
        btn_add=tk.Button(toolbar, text='Добавить', bg='#d7d7d7', bd=0,image=self.img_add, command=self.open_child)
        
        # отображение кнопки на экране
        btn_add.pack(side=tk.LEFT)

        # создание кнопку редактирования
        self.img_upd = tk.PhotoImage(file='img/update.png')
        btn_upd = tk.Button(toolbar, text='Изменить', bg='#d7d7d7', bd=0, image=self.img_upd, command=self.open_update_child)
        btn_upd.pack(side=tk.LEFT)

        # создание кнопки удаления данных
        self.img_del = tk.PhotoImage(file='img/delete.png')
        btn_del = tk.Button(toolbar, text='Удалить', bg='#d7d7d7', bd=0, image=self.img_del, command=self.delete_records)
        btn_del.pack(side=tk.LEFT)
        
        # создание кнопку поиска данных
        self.img_search = tk.PhotoImage(file='img/search.png')
        btn_search = tk.Button(toolbar, text='Найти', bg='#d7d7d7', bd=0, image=self.img_search, command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # создание кнопки обновления
        self.img_refresh = tk.PhotoImage(file='img/refresh.png')
        btn_refresh = tk.Button(toolbar, text='Найти', bg='#d7d7d7', bd=0, image=self.img_refresh, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # создаем таблицу
        self.tree = ttk.Treeview(self, columns=('id', 'name', 'phone', 'email', 'salary'), height=17, show='headings')

        # подписи и выравнивание колонок
        self.tree.column('id', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER) 
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        self.tree.heading('id', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        # отрисуем колонки
        self.tree.pack(side=tk.LEFT)

        # добавляем scroll bar
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)


    # создаем метод записи в бд с помощью GUI 
    def records(self, name, phone, email, salary):
        # команда передачи атрибутов
        self.db.insert_data(name, phone, email, salary)
        # добавляем метод для вывод данных в видже
        self.view_records()
    

    # создаем метод для ввода изменений в бд
    def update_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        # делаем запрос в бд
        self.db.cur.execute('''UPDATE employees SET name=?, phone=?, email=?,salary=? WHERE id=?''', (name, phone, email,salary, id))
        
        # сохраняем изменения
        self.db.conn.commit()

        # отображаем изменения в виджете
        self.view_records()


    # создаем метод для удаления записи в бд
    def delete_records(self):
        # цикл по выделенным записям
        for row in self.tree.selection():
            # удаление записи из бд
            self.db.cur.execute('''DELETE FROM employees WHERE id=?''', (self.tree.set(row, '#1')))

        # сохранение изменений в бд
        self.db.conn.commit()

        # обновление виджета таблицы
        self.view_records()
 

    # создаем метод вывода данных в виджет таблицы
    def view_records(self):
        # выбираем информацию из бд
        self.db.cur.execute('''SELECT * FROM employees''')
        # удаляем все из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавляем в виджет таблицы всю информацию из бд
        [self.tree.insert('', 'end', values=i) for i  in self.db.cur.fetchall()]


    # создаем метод поиска данных
    def search_records(self, name):
        # делаем запрос на вывод всей информации из бд
        self.db.cur.execute('SELECT * FROM employees WHERE name LIKE ?', ('%' + name + '%',))
        # удаляем все из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавляем в виджет таблицы всю информацию из бд
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]


    # создаем метод вызывающий дочерние окона
    def open_child(self):
        # вызываем класс Child
        Child()


 # метод вызывающий дочернее окно для редактирования данных
    def open_update_child(self):
        # вызываем класс Update
        Update()


    # метод вызывающий дочернее окно для поиска данных
    def open_search(self):
        # вызываем класс Search
        Search()



# создаем класс дочерних окон
class Child(tk.Toplevel):
    # создаем метод инициализации
    def __init__(self):
        super().__init__(root)
        # вызов метода инициализации дочерних окон из основного класса
        self.init_child()
        # добавляем атрибут 
        self.view = app


     # создаем метод для хранения и инициализации объектов GUI дочерних окон
    def init_child(self):
        # создаем заголовок окна
        self.title('Добавление сотрудника')
         # устанавливаем размер окна
        self.geometry('400x200')
        # ограничение изменения размера окна
        self.resizable(False, False)

        # перехват событий из приложения, фокус переводится на только что открытое окно
        self.grab_set()

        # захватываем фокус
        self.focus_set()

        # добавляем подписи
        Label_name = tk.Label(self, text='ФИО:')
        Label_name.place(x=50, y=50)
        Label_phone = tk.Label(self, text="Телефон")
        Label_phone.place(x=50, y=80)
        Label_email = tk.Label(self, text="E-mail")
        Label_email.place(x=50, y=110)
        Label_salary = tk.Label(self, text="Зарплата")
        Label_salary.place(x=50, y=140)
        
        # добавляем строки ввода и изменяем их положение
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        # создаем кнопку закрытия дочернего окна
        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        # меняем координаты
        btn_cancel.place(x=200, y=165)
       
        # создаем кнопку добавления
        self.btn_add = tk.Button(self, text='Добавить')
        # срабатывание кноки добавления по ЛКМ
        # при нажатии кнопки вызывается метод records, которому передаются значения из строк ввода
        self.btn_add.bind('<Button-1>', lambda ev: self.view.records(self.entry_name.get(),
                                                             self.entry_phone.get(),
                                                             self.entry_email.get(),
                                                             self.entry_salary.get()))
        # меняем координаты
        self.btn_add.place(x=265, y=165)




# Создаем класс для редактирования бд
class Update(Child):
    # создаем метод инициализации
    def __init__(self):
        super().__init__()
        # вызов метода инициализации  из основного класса
        self.init_edit()
        # добавляем объект базы данных
        self.db = db
        self.default_data()


    # создаем метод редактирования
    def init_edit(self):
        # создаем заголовок окна
        self.title('Изменение текущего сотрудника')
        
        # добавляем кнопку редактирования
        self.btn_edit = tk.Button(self, text='Изменить')
        # меняем ее положение
        self.btn_edit.place(x=265, y=165)
        # при редактировании данные ввода передаются records
        self.btn_edit.bind('<Button-1>', lambda ev: self.view.update_record(self.entry_name.get(),
                                                             self.entry_phone.get(),
                                                             self.entry_email.get(),
                                                             self.entry_salary.get()))
        # закрываем окно редактирования
        # add='+' позволяетна одну кнопку вешать более одного события
        self.btn_edit.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_add.destroy()


    # создаем метод для подгрузки данных в форму для редактирования
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        # делаем запрос бд
        self.db.cur.execute('''SELECT * from employees WHERE id = ?''', (id))
        row = self.db.cur.fetchone()

        # получаем доступ к первой записи из выборки
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])



# создаем класс поиска данных
class Search(tk.Toplevel):
    # создаем метод инициализации
    def __init__(self):
        super().__init__(root)
        # вызываем метод из класса
        self.init_search()
        # добавляем атрибут
        self.view = app
     
    
    # создаем метод поиска
    def init_search(self):
        # создаем заголовок окна
        self.title('Поиск сотрудника')
        # устанавливаем размер окна
        self.geometry('300x100')
        # ограничение изменения размера окна
        self.resizable(False, False)

        # перехват событий из приложения, фокус переводится на только что открытое окно
        self.grab_set()

        # захватываем фокус
        self.focus_set()

        # добавляем подписи
        Label_name = tk.Label(self, text='ФИО:')
        Label_name.place(x=30, y=30)
       
        # добавляем строку ввода для наименования и меняем ее положение
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=130, y=30)
        
        # создаем кнопку закрытия окна и меняем ее положение
        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=150, y=70)
       
        # создаем кнопку поиска
        self.btn_add = tk.Button(self, text='Поиск')
        # срабатывание кноки добавления по ЛКМ
        # при нажатии кнопки вызывается метод search_records, которому передаются значения из строк ввода
        self.btn_add.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get()))
                                                           
        # меняем координаты
        self.btn_add.place(x=225, y=70)



# создаем класс баз данных
class Db():
    # создаем метод инициализации
    def  __init__(self):
        # присоединяем базу данных
        self.conn = sqlite3.connect('List of employees.db')
        # создаем переменную для запросов sql
        self.cur = self.conn.cursor()
        # вызываем команду создания таблицы
        self.cur.execute('''CREATE TABLE IF NOT EXISTS employees(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    salary INTEGER)''')
        # сохраняем изменения
        self.conn.commit()
    

    # создаем метод добавления данных в бд
    def insert_data(self, name, phone, email, salary):
        # добавляем элементы в бд
        self.cur.execute('''INSERT INTO employees(name, phone, email, salary) 
        VALUES(?, ?, ?, ?)''', (name, phone, email, salary))
        # сохраняем изменения
        self.conn.commit()

        

# создаем окно
if  __name__ == '__main__':
    # cоздаем обьект класса Tk (окно)
    root = tk.Tk()  
    db = Db()
    # создаем объекта класса Main
    app = Main(root)
    app.pack()
    # Заголовок окна
    root.title('Список сотрудников компании')
    # Размер окна
    root.geometry('820x400') # задаем размеры окна
    # Ограничение изменения размеров окна
    root.resizable(False, False)
    # запуск цикла событий
    root.mainloop() 