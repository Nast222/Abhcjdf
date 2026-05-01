import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

BOOKS_FILE = "books.json"

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_books()

        # --- Поля ввода ---
        tk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry = tk.Entry(root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.genre_entry = tk.Entry(root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.pages_entry = tk.Entry(root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # --- Кнопка добавления ---
        self.add_btn = tk.Button(root, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # --- Фильтры ---
        tk.Label(root, text="Фильтр по жанру:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.filter_genre = tk.Entry(root, width=20)
        self.filter_genre.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(root, text="Больше страниц:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.filter_pages = tk.Entry(root, width=10)
        self.filter_pages.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        self.filter_btn = tk.Button(root, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=7, column=0, columnspan=2, pady=5)

        # --- Таблица книг ---
        self.tree = ttk.Treeview(root, columns=("title", "author", "genre", "pages"), show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        self.tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Заполнение таблицы
        self.update_tree()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_str = self.pages_entry.get().strip()

        if not all([title, author, genre, pages_str]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            pages = int(pages_str)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return

        book
