import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import time
import  os


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Catalog Creator")
        self.root.geometry("400x300")
        self.root.attributes("-alpha", 0.5)  # Начальная прозрачность 0

        # Центрирование главного окна
        self.center_window()

        # Лоадер
        self.loader_label = tk.Label(root, text="Welcome to beta version", font=("Arial", 16))
        self.loader_label.pack(pady=20)

        # Анимация появления окна
        self.fade_in()

        # Кнопки
        self.create_button = tk.Button(root, text="Создать каталог", command=self.open_catalog_window)
        self.create_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Сохранить", command=self.save_file)
        self.save_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Выход", command=self.exit_app)
        self.exit_button.pack(pady=10)
    # def loading_window(self):
    #     # Окно загрузки
    #     loading_window = tk.Toplevel(self.root)
    #     loading_window.title("loading")
    #     loading_window.geometry("75x120")
    #     loading_window.attributes("-alpha", 0) # Начальная прозрачность окна загрузки

    def center_window(self):
        # Центрирование окна на экране
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 400) // 2  # Ширина окна 400
        y = (screen_height - 300) // 2  # Высота окна 300
        self.root.geometry(f"+{x}+{y}")

    def fade_in(self):
        # Плавное появление главного окна
        for i in range(1, 11):
            self.root.attributes("-alpha", i * 0.1)
            self.root.update()
            time.sleep(0.05)  # Задержка для плавного эффекта

    def open_catalog_window(self):
        catalog_window = tk.Toplevel(self.root)
        catalog_window.title("Catalog Window")
        catalog_window.geometry("600x300")
        catalog_window.attributes("-alpha", 0)  # Начальная прозрачность

        # Центрирование нового окна
        self.center_catalog_window(catalog_window)

        # Анимация появления нового окна
        self.fade_in_window(catalog_window)

        # Создание вкладок
        notebook = ttk.Notebook(catalog_window)

        movies_tab = ttk.Frame(notebook)
        books_tab = ttk.Frame(notebook)
        animation_tab = ttk.Frame(notebook)

        notebook.add(movies_tab, text="1")
        notebook.add(books_tab, text="2")
        notebook.add(animation_tab, text="3")

        # Описание для вкладок
        movies_desc = ttk.Label(movies_tab, text="list 1")
        books_desc = ttk.Label(books_tab, text="list 2")
        animation_desc = ttk.Label(animation_tab, text="list 3")

        # Создание Treeview
        self.movies_list = ttk.Treeview(movies_tab)
        self.books_list = ttk.Treeview(books_tab)
        self.animation_list = ttk.Treeview(animation_tab)

        self.movies_list['columns'] = ('a', 'b', 'c')
        self.books_list['columns'] = ('z', 'x', 'v')
        self.animation_list['columns'] = ('n', 'g', 'r')

        # Настройка столбцов для Treeview
        for tree in [self.movies_list, self.books_list, self.animation_list]:
            for i, col in enumerate(tree['columns']):
                tree.column(col, width=100, anchor='center')
                tree.heading(col, text=col.capitalize())
            # Пример добавления данных
            if tree == self.movies_list:
                tree.insert('', 'end', text='first', values=('pov', 'fov', 'uwu'))
            elif tree == self.books_list:
                tree.insert('', 'end', text='your text', values=('your text', 'your text', 'your text'))
            elif tree == self.animation_list:
                tree.insert('', 'end', text='list of p its trash', values=('your text', '+', '-'))

        # Упаковка виджетов
        movies_desc.pack()
        self.movies_list.pack()
        books_desc.pack()
        self.books_list.pack()
        animation_desc.pack()
        self.animation_list.pack()

        notebook.pack(fill='both', expand=True)

    def center_catalog_window(self, window):
        # Центрирование нового окна
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - 600) // 2  # Ширина окна 600
        y = (screen_height - 300) // 2  # Высота окна 300
        window.geometry(f"+{x}+{y}")

    def fade_in_window(self, window):
        # Плавное появление нового окна
        for i in range(1, 10):
            window.attributes("-alpha", i * 0.3)
            window.update()
            time.sleep(0.02)  # Задержка для плавного эффекта

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".cat",
                                                   filetypes=[("Catalog files", "*.cat"), ("All files", "*.*")])
        if file_path:
            # Здесь можно добавить код для сохранения содержимого каталогов
            with open(file_path, 'w') as file:
                file.write("Содержимое вашего каталога.")  # Здесь можно добавить фактическое содержимое
            messagebox.showinfo("Успех", "Файл сохранен!")

    def exit_app(self):
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()