import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import time
import json
import os

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Catalog Creator v2.1.0")
        self.root.geometry("400x300")

        
        self.center_window()

       
        self.loader_label = tk.Label(root, text="Welcome to beta version", font=("Arial", 16))
        self.loader_label.pack(pady=20)

        
        self.fade_in()

        # Кнопки
        self.create_button = self.create_button_with_hover("Создать каталог", self.open_catalog_window)
        self.create_button.pack(pady=10)

        self.save_button = self.create_button_with_hover("Сохранить", self.save_file)
        self.save_button.pack(pady=10)

        self.view_button = self.create_button_with_hover("Посмотреть последние каталоги", self.view_recent_catalogs)
        self.view_button.pack(pady=10)

        self.exit_button = self.create_button_with_hover("Выход", self.exit_app)
        self.exit_button.pack(pady=10)

     
        self.info_button = self.create_info_button()
        self.info_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Размещение в правом нижнем углу

        
        self.support_button = self.create_support_button()
        self.support_button.place(relx=0.0, rely=1.0, anchor='sw', x=10, y=-10)  # Размещение в левом нижнем углу

        # Данные каталога
        self.movie_data = [
            {"name": "Film 1", "genre": "Action", "year": "2020"},
            {"name": "Film 2", "genre": "Comedy", "year": "2021"}
        ]

        self.book_data = [
            {"name": "Book 1", "author": "Author 1", "year": "2018"},
            {"name": "Book 2", "author": "Author 2", "year": "2019"}
        ]

        self.animation_data = [
            {"name": "Animation 1", "studio": "Studio A", "year": "2017"}
        ]

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        self.root.geometry(f"+{x}+{y}")

    def fade_in(self, step=0.1, delay=0.05):
        for i in range(1, 11):
            self.root.attributes("-alpha", i * step)
            self.root.update()
            time.sleep(delay)

    def open_catalog_window(self):
        catalog_window = tk.Toplevel(self.root)
        catalog_window.title("Catalog Window")
        catalog_window.geometry("600x300")

        
        self.toggle_transparency_button = tk.Button(catalog_window, text="Показать ползунок прозрачности",
                                                    command=self.show_transparency_slider)
        self.toggle_transparency_button.pack(pady=5)

        
        self.transparency_scale = tk.Scale(catalog_window, from_=0.0, to=1.0, resolution=0.1,
                                            orient='horizontal', label='Степень прозрачности', bg='lightblue',
                                            activebackground='deepskyblue', troughcolor='lightgray')
        self.transparency_scale.set(1.0)  
        self.transparency_scale.pack(pady=5)
        self.transparency_scale.pack_forget()  

        
        self.apply_transparency_button = tk.Button(catalog_window, text="Применить прозрачность",
                                                    command=lambda: self.set_transparency(catalog_window))
        self.apply_transparency_button.pack(pady=5)

       
        notebook = ttk.Notebook(catalog_window)

        movies_tab = ttk.Frame(notebook)
        books_tab = ttk.Frame(notebook)
        animation_tab = ttk.Frame(notebook)

        notebook.add(movies_tab, text="Фильмы")
        notebook.add(books_tab, text="Книги")
        notebook.add(animation_tab, text="Анимация")

       
        self.movies_list = ttk.Treeview(movies_tab, columns=("name", "genre", "year"))
        self.books_list = ttk.Treeview(books_tab, columns=("name", "author", "year"))
        self.animation_list = ttk.Treeview(animation_tab, columns=("name", "studio", "year"))

        
        self.setup_treeview(self.movies_list, ["Название", "Жанр", "Год"])
        self.setup_treeview(self.books_list, ["Название", "Автор", "Год"])
        self.setup_treeview(self.animation_list, ["Название", "Студия", "Год"])

       
        self.populate_treeview(self.movies_list, self.movie_data)
        self.populate_treeview(self.books_list, self.book_data)
        self.populate_treeview(self.animation_list, self.animation_data)

        
        self.movies_list.pack(fill='both', expand=True)
        self.books_list.pack(fill='both', expand=True)
        self.animation_list.pack(fill='both', expand=True)

        notebook.pack(fill='both', expand=True)

        
        self.movies_list.bind("<Double-1>", lambda event: self.edit_item(self.movies_list, self.movie_data, "фильм"))
        self.books_list.bind("<Double-1>", lambda event: self.edit_item(self.books_list, self.book_data, "книгу"))
        self.animation_list.bind("<Double-1>",
                                 lambda event: self.edit_item(self.animation_list, self.animation_data, "анимацию"))

    def show_transparency_slider(self):
        self.transparency_scale.pack(pady=5) 

    def setup_treeview(self, treeview, columns):
        for i, col in enumerate(columns):
            treeview.column(i, width=150, anchor='center')
            treeview.heading(i, text=col)

        treeview.column('#0', width=0, stretch=tk.NO)
        treeview['show'] = 'headings'

    def populate_treeview(self, treeview, data):
        treeview.delete(*treeview.get_children())  # Очистка текущих данных
        for item in data:
            values = tuple(item.values())
            treeview.insert('', 'end', values=values)

    def set_transparency(self, window):
        transparency_value = self.transparency_scale.get()
        window.attributes("-alpha", transparency_value)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            catalog_data = {
                "movies": self.movie_data,
                "books": self.book_data,
                "animations": self.animation_data
            }
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(catalog_data, file, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Файл сохранен!")
            self.update_recent_catalogs(file_path)  # Обновление списка последних каталогов

    def exit_app(self):
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()

    def edit_item(self, treeview, data, item_type):
        selected_item = treeview.selection()
        if selected_item:
            item_values = treeview.item(selected_item, 'values')

            # Создание нового окна для редактирования
            edit_window = tk.Toplevel(self.root)
            edit_window.title(f"Редактировать {item_type}")

            fields = [("Название", item_values[0]), ("Жанр/Автор/Студия", item_values[1]), ("Год", item_values[2])]
            entries = []
            for field_name, value in fields:
                label = tk.Label(edit_window, text=field_name + ":")
                label.pack()
                entry = tk.Entry(edit_window)
                entry.insert(0, value)
                entry.pack()
                entries.append(entry)

            save_button = tk.Button(edit_window, text="Сохранить",
                                    command=lambda: self.save_edited_item(selected_item, entries, data))
            save_button.pack()

    def save_edited_item(self, selected_item, entries, data):
        new_values = [entry.get() for entry in entries]
        if all(new_values):
            treeview = self.movies_list if 'фильм' in selected_item else self.books_list if 'книга' in selected_item else self.animation_list
            treeview.item(selected_item, values=new_values)

            # Обновление данных
            if treeview == self.movies_list:
                index = self.movies_list.index(selected_item)
                data[index] = {"name": new_values[0], "genre": new_values[1], "year": new_values[2]}
            elif treeview == self.books_list:
                index = self.books_list.index(selected_item)
                data[index] = {"name": new_values[0], "author": new_values[1], "year": new_values[2]}
            elif treeview == self.animation_list:
                index = self.animation_list.index(selected_item)
                data[index] = {"name": new_values[0], "studio": new_values[1], "year": new_values[2]}

            messagebox.showinfo("Успех", "Элемент успешно обновлен!")
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

    def create_button_with_hover(self, text, command):
        button = tk.Button(self.root, text=text, command=command, bg='lightgray', activebackground='deepskyblue')
        button.bind("<Enter>", lambda e: button.config(bg='lightblue'))
        button.bind("<Leave>", lambda e: button.config(bg='lightgray'))
        return button

    def create_info_button(self):
        info_button = tk.Button(self.root, text="ℹ️", command=self.show_info, width=2, bg='lightgray',
                                activebackground='deepskyblue')
        info_button.config(font=("Arial", 12))
        return info_button

    def create_support_button(self):
        support_button = tk.Button(self.root, text="🛠️", command=self.support_info, width=2, bg='lightgray',
                                   activebackground='deepskyblue')
        support_button.config(font=("Arial", 12))
        return support_button

    def support_info(self):
        messagebox.showinfo("Техподдержка", "Свяжитесь с нами по email:")

    def show_info(self):
        messagebox.showinfo("Информация", "Креатор каталогов\nВерсия 1.0\n\n"
                                            "Планируемые улучшения:\n- Добавить возможность импорта/экспорта\n"
                                            "- Улучшение интерфейса\n"
                                            "- Добавить возможность поиска по каталогу")

    def view_recent_catalogs(self):
        recent_catalogs = self.get_recent_catalogs()
        if recent_catalogs:
            recent_window = tk.Toplevel(self.root)
            recent_window.title("Последние каталоги")
            recent_window.geometry("400x300")

            label = tk.Label(recent_window, text="Последние созданные каталоги:", font=("Arial", 14))
            label.pack(pady=10)

            listbox = tk.Listbox(recent_window)
            for catalog in recent_catalogs:
                listbox.insert(tk.END, catalog)
            listbox.pack(fill=tk.BOTH, expand=True)

        else:
            messagebox.showinfo("Нет данных", "Пока нет созданных каталогов.")

    def update_recent_catalogs(self, file_path):
        recent_files_path = "recent_catalogs.txt"
        with open(recent_files_path, 'a') as f:
            f.write(file_path + "\n")

    def get_recent_catalogs(self):
        recent_files_path = "recent_catalogs.txt"
        if os.path.exists(recent_files_path):
            with open(recent_files_path, 'r') as f:
                return [line.strip() for line in f.readlines()]
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
