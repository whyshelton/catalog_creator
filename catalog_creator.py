import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import time
import json


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Catalog Creator")
        self.root.geometry("400x300")

        
        self.center_window()

        
        self.loader_label = tk.Label(root, text="Welcome to beta version", font=("Arial", 16))
        self.loader_label.pack(pady=20)

        
        self.fade_in()

        
        self.create_button = tk.Button(root, text="Создать каталог", command=self.open_catalog_window)
        self.create_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Сохранить", command=self.save_file)
        self.save_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Выход", command=self.exit_app)
        self.exit_button.pack(pady=10)

        
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

        #
        self.toggle_transparency_button = tk.Button(catalog_window, text="Toggle Transparency",
                                                    command=lambda: self.toggle_transparency(catalog_window))
        self.toggle_transparency_button.pack(pady=5)

        
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

    def setup_treeview(self, treeview, columns):
        for i, col in enumerate(columns):
            treeview.column(i, width=150, anchor='center')
            treeview.heading(i, text=col)

        treeview.column('#0', width=0, stretch=tk.NO)
        treeview['show'] = 'headings'

    def populate_treeview(self, treeview, data):
        treeview.delete(*treeview.get_children())  
        for item in data:
            values = tuple(item.values())
            treeview.insert('', 'end', values=values)

    def toggle_transparency(self, window):
        current_alpha = window.attributes("-alpha")
        if current_alpha == 1.0:
            window.attributes("-alpha", 0.7)  
        else:
            window.attributes("-alpha", 1.0)  

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

    def exit_app(self):
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()

    def edit_item(self, treeview, data, item_type):
        selected_item = treeview.selection()
        if selected_item:
            item_values = treeview.item(selected_item, 'values')

            
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
            item_index = int(self.movies_list.index(selected_item))
            data[item_index]['name'] = new_values[0]
            data[item_index][
                'genre' if 'genre' in data[item_index] else 'author' if 'author' in data[item_index] else 'studio'] = \
            new_values[1]
            data[item_index]['year'] = new_values[2]

            self.populate_treeview(self.movies_list, self.movie_data)
            self.populate_treeview(self.books_list, self.book_data)
            self.populate_treeview(self.animation_list, self.animation_data)

            messagebox.showinfo("Успех", "Элемент успешно обновлен!")
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
