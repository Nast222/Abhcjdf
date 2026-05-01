import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = []
        self.load_expenses()

        # --- Поля ввода ---
        tk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = tk.Entry(root, width=20)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.category_entry = tk.Entry(root, width=20)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = tk.Entry(root, width=20)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # --- Кнопка добавления ---
        self.add_btn = tk.Button(root, text="Добавить расход", command=self.add_expense)
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # --- Фильтры ---
        tk.Label(root, text="Фильтр по категории:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.filter_category = tk.Entry(root, width=20)
        self.filter_category.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(root, text="Период (ГГГГ-ММ-ДД):").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.filter_start = tk.Entry(root, width=12)
        self.filter_start.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.filter_end = tk.Entry(root, width=12)
        self.filter_end.grid(row=5, column=1, padx=85, pady=5, sticky="w")

        self.filter_btn = tk.Button(root, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=6, column=0, columnspan=2, pady=5)

        # --- Таблица расходов ---
        self.tree = ttk.Treeview(root, columns=("amount", "category", "date"), show="headings")
        self.tree.heading("amount", text="Сумма")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # --- Итоговая сумма ---
        self.total_label = tk.Label(root, text="Итого: 0.00 ₽", font=("Arial", 12))
        self.total_label.grid(row=8, column=0, columnspan=2, pady=10)

        # Заполнение таблицы и подсчёт суммы
        self.update_tree()

    def add_expense(self):
        amount_str = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        date_str = self.date_entry.get().strip()

        if not all([amount_str, category, date_str]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной.")
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            date_str = date.isoformat()
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {e}")
            return

        expense = {"amount": amount, "category": category, "date": date_str}
        self.expenses.append(expense)
        self.save_expenses()
        self.update_tree()

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        total = 0.0
        for exp in self.expenses:
            self.tree.insert("", "end", values=(f"{exp['amount']:.2f} ₽", exp['category'], exp['date']))
            total += exp['amount']

        self.total_label.config(text=f"Итого: {total:.2f} ₽")

    def apply_filter(self):
        cat_filter = self.filter_category.get().strip().lower()

        try:
            start_date = datetime.strptime(self.filter_start.get().strip(), "%Y-%m-%d").date() if self.filter_start.get().strip() else None
            end_date = datetime.strptime(self.filter_end.get().strip(), "%Y-%m-%d").date() if self.filter_end.get().strip() else None
            if start_date and end_date and start_date > end_date:
                raise ValueError("Начальная дата не может быть позже конечной.")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный формат даты: {e}")
            return

        filtered = self.expenses

        if cat_filter:
            filtered = [e for e in filtered if cat_filter in e["category"].lower()]

        if start_date:
            filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d").date() >= start_date]

        if end_date:
            filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d").date() <= end_date]

        for i in self.tree.get_children():
            self.tree.delete(i)

        total = 0.0
        for exp in filtered:
            self.tree.insert("", "end", values=(f"{exp['amount']:.2f} ₽", exp['category'], exp['date']))
            total += exp['amount']

    def save_expenses(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)

    def load_expenses(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                try:
                    self.expenses = json.load(f)
                except json.JSONDecodeError:
                    self.expenses = []

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
