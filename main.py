import tkinter as tk
from tkinter import ttk
import sqlite3

# Создание класса главного окна приложения
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Инициализация главного окна
    def init_main(self):
        # Создание панели инструментов
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Загрузка изображения для кнопки добавления
        self.add_img = tk.PhotoImage(file="./img/add.png")
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)

        # Создание виджета Treeview для отображения данных
        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "tel", "email", "salary"), height=45, show="headings"
        )

        # Настройка колонок таблицы
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=250, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=110, anchor=tk.CENTER)

        # Установка заголовков таблицы
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Заработная плата")
        # Размещение Treeview на главном окне
        self.tree.pack(side=tk.LEFT)

        # Загрузка изображения для кнопки редактирования
        self.update_img = tk.PhotoImage(file="./img/update.png")
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)

        # Загрузка изображения для кнопки удаления
        self.delete_img = tk.PhotoImage(file="./img/delete.png")
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)

        # Загрузка изображения для кнопки поиска
        self.search_img = tk.PhotoImage(file="./img/search.png")
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)

    # Метод для открытия окна добавления нового контакта
    def open_dialog(self):
        Child()

    # Метод для добавления новой записи
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # Метод для отображения записей в Treeview
    def view_records(self):
        self.db.cursor.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

    # Метод для открытия окна редактирования контакта
    def open_update_dialog(self):
        Update()

    # Метод для обновления записи в базе данных
    def update_records(self, name, tel, email, salary):
        self.db.cursor.execute(
            """UPDATE db SET name=?, tel=?, email=?, salary=? WHERE id=?""",
            (name, tel, email, salary, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()
        self.view_records()

    # Метод для удаления записи из базы данных
    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1"))
            )
        self.db.conn.commit()
        self.view_records()

    # Метод для открытия окна поиска контакта
    def open_search_dialog(self):
        Search()

    # Метод для поиска контактов в базе данных по имени
    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

# Класс для окна добавления нового контакта
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Инициализация окна добавления
    def init_child(self):
        self.title("Добавить")
        self.geometry("400x220")
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        # Создание меток и полей ввода для ФИО, телефона и E-mail
        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=110)
        label_sal = tk.Label(self, text='Заработная плата:')
        label_sal.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)
        self.entry_sal = ttk.Entry(self)
        self.entry_sal.place(x=200, y=140)

        # Кнопка "Закрыть"
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        # Кнопка "Добавить"
        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

        # Привязка действия к кнопке "Добавить"
        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_sal.get()
            ),
        )

# Класс для окна редактирования контакта
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    # Инициализация окна редактирования
    def init_edit(self):
        self.title("Редактирование контакта")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=170)
        
        # Привязка действия к кнопке "Редактировать"
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_sal.get()
            ),
        )
        
        # Привязка действия к кнопке "Редактировать" для закрытия окна
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
        
        # Удаление кнопки "Добавить"
        self.btn_ok.destroy()

    # Заполнение полей данными из выбранной записи
    def default_data(self):
        self.db.cursor.execute(
            "SELECT * FROM db WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),
        )
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_sal.insert(0, row[4])

# Класс для окна поиска контакта
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    # Инициализация окна поиска
    def init_search(self):
        self.title("Поиск контакта")
        self.geometry("300x100")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        # Кнопка "Закрыть"
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        # Кнопка "Найти"
        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=105, y=50)
        
        # Привязка действия к кнопке "Найти"
        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        
        # Привязка действия к кнопке "Найти" для закрытия окна
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")

# Класс для работы с базой данных SQLite
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("db.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT,
                salary INTEGER
            )"""
        )
        self.conn.commit()

    # Метод для вставки данных в базу данных
    def insert_data(self, name, tel, email, salary):
        self.cursor.execute(
            """INSERT INTO db(name, tel, email, salary) VALUES(?, ?, ?, ?)""", (name, tel, email, salary)
        )
        self.conn.commit()

# Основная часть программы, запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников компании")
    root.geometry("800x500")
    root.resizable(False, False)
    root.mainloop()
