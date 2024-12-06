
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from tkcalendar import DateEntry
from datetime import datetime

# Конфигурация базы данных
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Ваш пользователь MySQL
    'password': 'admin',  # Ваш пароль MySQL
    'database': 'buhgalteria'  # Имя базы данных
}

current_user = None  # Данные текущего пользователя


# Подключение к базе данных
def connect_to_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        messagebox.showerror("Ошибка", f"Не удалось подключиться к базе данных: {e}")
        return None


# Регистрация пользователя
def register_user():
    def submit_registration():
        username = reg_username_entry.get()
        password = reg_password_entry.get()
        if not username or not password:
            messagebox.showwarning("Ошибка", "Все поля обязательны для заполнения.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                messagebox.showinfo("Успешно", "Пользователь успешно зарегистрирован.")
                reg_window.destroy()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
            except mysql.connector.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка регистрации: {e}")
            finally:
                conn.close()

    reg_window = tk.Toplevel()
    reg_window.title("Регистрация")
    reg_window.geometry("300x200")
    reg_window.configure(bg="#fcf0f8")  # Устанавливаем цвет фона окна регистрации

    # Метки и поля ввода
    tk.Label(
        reg_window,
        text="Логин:",
        font=("Arial", 12),
        bg="#fcf0f8"
    ).pack(pady=5)

    reg_username_entry = tk.Entry(
        reg_window,
        font=("Arial", 12)
    )
    reg_username_entry.pack(pady=5)

    tk.Label(
        reg_window,
        text="Пароль:",
        font=("Arial", 12),
        bg="#fcf0f8"
    ).pack(pady=5)

    reg_password_entry = tk.Entry(
        reg_window,
        show="*",
        font=("Arial", 12)
    )
    reg_password_entry.pack(pady=5)

    # Кнопка регистрации
    tk.Button(
        reg_window,
        text="Зарегистрироваться",
        font=("Arial", 12),
        command=submit_registration,
        bg="#fcf0f8"
    ).pack(pady=10)


# Вход пользователя
def login_user():
    global current_user
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showwarning("Ошибка", "Введите имя пользователя и пароль.")
        return

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user:
                current_user = user
                messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
                login_window.destroy()
                open_main_app()
            else:
                messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")
        except mysql.connector.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка выполнения запроса: {e}")
        finally:
            conn.close()


# Добавление расхода
from tkcalendar import DateEntry  # Добавлено

def add_expense():
    def save_expense():
        category = category_combo.get()
        amount = amount_entry.get()
        description = description_entry.get()
        date = date_entry.get_date()  # Получаем дату из календаря

        if not category or not amount:
            messagebox.showwarning("Ошибка", "Заполните все поля.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO expenses (category_id, amount, expense_date, description_, user_id) "
                    "VALUES ((SELECT category_id FROM categories WHERE category_name = %s), %s, %s, %s, %s)",
                    (category, amount, date, description, current_user['user_id'])
                )
                conn.commit()
                messagebox.showinfo("Успех", "Расход добавлен.")
                expense_window.destroy()
                load_expenses()
            except mysql.connector.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")
            finally:
                conn.close()

    expense_window = tk.Toplevel()
    expense_window.title("Добавить расход")
    expense_window.geometry("400x350")
    expense_window.configure(bg="#fcf0f8")  # Устанавливаем цвет фона окна

    # Метки и элементы управления
    tk.Label(expense_window, text="Категория:", font=("Arial", 12), bg="#fcf0f8").pack(pady=5)
    category_combo = ttk.Combobox(expense_window, font=("Arial", 12))
    category_combo.pack(pady=5)
    category_combo['values'] = get_categories()

    tk.Label(expense_window, text="Сумма:", font=("Arial", 12), bg="#fcf0f8").pack(pady=5)
    amount_entry = tk.Entry(expense_window, font=("Arial", 12))
    amount_entry.pack(pady=5)

    tk.Label(expense_window, text="Дата:", font=("Arial", 12), bg="#fcf0f8").pack(pady=5)
    date_entry = DateEntry(expense_window, font=("Arial", 12), date_pattern="yyyy-mm-dd")  # Календарь
    date_entry.pack(pady=5)

    tk.Label(expense_window, text="Описание:", font=("Arial", 12), bg="#fcf0f8").pack(pady=5)
    description_entry = tk.Entry(expense_window, font=("Arial", 12))
    description_entry.pack(pady=5)

    tk.Button(
        expense_window,
        text="Сохранить",
        font=("Arial", 12),
        command=save_expense,
        bg="#fcf0f8"
    ).pack(pady=10)

# Загрузка категорий
def get_categories():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT category_name FROM categories")
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки категорий: {e}")
            return []
        finally:
            conn.close()


# Загрузка расходов
def load_expenses():
    for row in expense_tree.get_children():
        expense_tree.delete(row)

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT e.expense_id, c.category_name, e.amount, e.expense_date, e.description_ "
                "FROM expenses e "
                "JOIN categories c ON e.category_id = c.category_id "
                "WHERE e.user_id = %s",
                (current_user['user_id'],)
            )
            for row in cursor.fetchall():
                expense_tree.insert("", "end", values=row)
        except mysql.connector.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки расходов: {e}")
        finally:
            conn.close()


def view_reports():
    def generate_report():
        start_date = start_date_entry.get_date()  # Получаем начальную дату
        end_date = end_date_entry.get_date()  # Получаем конечную дату
        category = category_combobox.get()  # Получаем выбранную категорию

        if not start_date or not end_date:
            messagebox.showwarning("Ошибка", "Выберите начальную и конечную дату.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Если выбрана конкретная категория
                if category != "Все категории":
                    cursor.execute(
                        """
                        SELECT c.category_name, e.expense_date, e.amount, e.description_
                        FROM expenses e
                        JOIN categories c ON e.category_id = c.category_id
                        WHERE e.user_id = %s AND e.expense_date BETWEEN %s AND %s AND c.category_name = %s
                        """,
                        (current_user['user_id'], start_date, end_date, category)
                    )
                else:
                    # Если выбраны все категории
                    cursor.execute(
                        """
                        SELECT c.category_name, e.expense_date, e.amount, e.description_
                        FROM expenses e
                        JOIN categories c ON e.category_id = c.category_id
                        WHERE e.user_id = %s AND e.expense_date BETWEEN %s AND %s
                        """,
                        (current_user['user_id'], start_date, end_date)
                    )

                # Очищаем старые данные в treeview
                for row in report_tree.get_children():
                    report_tree.delete(row)

                total_expenses = 0
                for category_name, expense_date, amount, description in cursor.fetchall():
                    report_tree.insert("", "end", values=(category_name, expense_date, amount, description))
                    total_expenses += amount

                # Обновляем общую сумму расходов
                total_label.config(text=f"Общая сумма расходов: {total_expenses:.2f} руб.")
            except mysql.connector.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка запроса: {e}")
            finally:
                conn.close()

    report_window = tk.Toplevel()
    report_window.title("Отчеты по расходам")
    report_window.geometry("600x600")
    report_window.configure(bg="#fcf0f8")

    # Заголовок окна отчета
    tk.Label(report_window, text="Отчеты по расходам", font=("Arial", 14), bg="#fcf0f8").pack(pady=10)

    # Поля для ввода дат
    tk.Label(report_window, text="Начальная дата:", font=("Arial", 12), bg="#fcf0f8").pack(pady=5)
    start_date_entry = DateEntry(report_window, font=("Arial", 12), date_pattern="yyyy-mm-dd")
    start_date_entry.pack(pady=5)

    tk.Label(report_window, text="Конечная дата:", font=("Arial", 12), bg="#fcf0f8").pack(pady=5)
    end_date_entry = DateEntry(report_window, font=("Arial", 12), date_pattern="yyyy-mm-dd")
    end_date_entry.pack(pady=5)

    # Выпадающий список для выбора категории
    tk.Label(report_window, text="Выберите категорию:", font=("Arial", 12), bg="#fcf0f8").pack(pady=5)

    # Получаем список категорий из базы данных
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT category_name FROM categories")
    categories = [row[0] for row in cursor.fetchall()]
    categories.insert(0, "Все категории")  # Добавляем опцию "Все категории"

    category_combobox = ttk.Combobox(report_window, values=categories, font=("Arial", 12))
    category_combobox.pack(pady=5)
    category_combobox.set("Все категории")  # Устанавливаем начальное значение

    # Кнопка для генерации отчета
    tk.Button(
        report_window,
        text="Сгенерировать отчет",
        font=("Arial", 12),
        command=generate_report,
        bg="#fcf0f8"
    ).pack(pady=10)

    # Treeview для отображения отчета
    report_tree = ttk.Treeview(report_window, columns=("Категория", "Дата", "Сумма", "Описание"), show="headings")
    report_tree.heading("Категория", text="Категория")
    report_tree.heading("Дата", text="Дата")
    report_tree.heading("Сумма", text="Сумма")
    report_tree.heading("Описание", text="Описание")
    report_tree.pack(fill="both", expand=True, pady=10)

    # Метка для отображения общей суммы расходов
    total_label = tk.Label(report_window, text="", font=("Arial", 12), bg="#fcf0f8")
    total_label.pack(pady=10)

def add_category():
    def save_category():
        category_name = category_entry.get()

        if not category_name:
            messagebox.showwarning("Ошибка", "Введите название категории.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO categories (category_name) VALUES (%s)", (category_name,))
                conn.commit()
                messagebox.showinfo("Успех", "Категория добавлена.")
                category_window.destroy()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Ошибка", "Такая категория уже существует.")
            except mysql.connector.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения категории: {e}")
            finally:
                conn.close()

    category_window = tk.Toplevel()
    category_window.title("Добавить категорию")
    category_window.geometry("300x150")
    category_window.configure(bg="#fcf0f8")

    # Метка для ввода названия категории
    tk.Label(category_window, text="Название категории:", font=("Arial", 12), bg="#fcf0f8").pack(pady=10)

    # Поле для ввода названия категории
    category_entry = tk.Entry(category_window, font=("Arial", 12))
    category_entry.pack(pady=10)

    # Кнопка для сохранения категории
    tk.Button(
        category_window,
        text="Сохранить",
        font=("Arial", 12),
        command=save_category,
        bg="#fcf0f8"
    ).pack(pady=10)

def edit_expense():
    selected_item = expense_tree.selection()
    if not selected_item:
        messagebox.showwarning("Ошибка", "Выберите расход для редактирования.")
        return

    expense_id = expense_tree.item(selected_item)["values"][0]  # Получаем ID выбранного расхода

    # Окно для редактирования расхода
    def save_edited_expense():
        category = category_combo.get()
        amount = amount_entry.get()
        description = description_entry.get()
        date = date_entry.get_date()

        if not category or not amount:
            messagebox.showwarning("Ошибка", "Заполните все поля.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE expenses
                    SET category_id = (SELECT category_id FROM categories WHERE category_name = %s),
                        amount = %s,
                        expense_date = %s,
                        description_ = %s
                    WHERE expense_id = %s
                    """,
                    (category, amount, date, description, expense_id)
                )
                conn.commit()
                messagebox.showinfo("Успех", "Расход обновлен.")
                edit_window.destroy()
                load_expenses()
            except mysql.connector.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка обновления: {e}")
            finally:
                conn.close()

    edit_window = tk.Toplevel()
    edit_window.title("Редактировать расход")
    edit_window.geometry("400x350")
    edit_window.configure(bg="#fcf0f8")

    # Загрузка текущих данных расхода
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT c.category_name, e.amount, e.expense_date, e.description_ "
                "FROM expenses e "
                "JOIN categories c ON e.category_id = c.category_id "
                "WHERE e.expense_id = %s", (expense_id,)
            )
            expense_data = cursor.fetchone()
            if expense_data:
                category_name, amount, expense_date, description = expense_data
            else:
                messagebox.showerror("Ошибка", "Расход не найден.")
                edit_window.destroy()
                return
        except mysql.connector.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {e}")
            edit_window.destroy()
            return
        finally:
            conn.close()

    # Элементы для редактирования
    tk.Label(edit_window, text="Категория:", font=("Arial", 12), bg="#fcf0f8").pack(pady=5)
    category_combo = ttk.Combobox(edit_window, font=("Arial", 12))
    category_combo.pack(pady=5)
    category_combo['values'] = get_categories()
    category_combo.set(category_name)

    tk.Label(edit_window, text="Сумма:", font=("Arial", 12), bg="#fcf0f8").pack(pady=5)
    amount_entry = tk.Entry(edit_window, font=("Arial", 12))
    amount_entry.pack(pady=5)
    amount_entry.insert(0, amount)

    tk.Label(edit_window, text="Дата:", font=("Arial", 12), bg="#fcf0f8").pack(pady=5)
    date_entry = DateEntry(edit_window, font=("Arial", 12), date_pattern="yyyy-mm-dd")
    date_entry.pack(pady=5)
    date_entry.set_date(expense_date)

    tk.Label(edit_window, text="Описание:", font=("Arial", 12), bg="#fcf0f8").pack(pady=5)
    description_entry = tk.Entry(edit_window, font=("Arial", 12))
    description_entry.pack(pady=5)
    description_entry.insert(0, description)

    tk.Button(
        edit_window,
        text="Сохранить изменения",
        font=("Arial", 12),
        command=save_edited_expense,
        bg="#fcf0f8"
    ).pack(pady=10)
#Удаление расхода
def delete_expense():
    selected_item = expense_tree.selection()
    if not selected_item:
        messagebox.showwarning("Ошибка", "Выберите расход для удаления.")
        return

    expense_id = expense_tree.item(selected_item)["values"][0]  # Получаем ID выбранного расхода

    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот расход?"):
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM expenses WHERE expense_id = %s", (expense_id,))
                conn.commit()
                messagebox.showinfo("Успех", "Расход удален.")
                load_expenses()
            except mysql.connector.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка удаления: {e}")
            finally:
                conn.close()



# Основное приложение
def open_main_app():
    app = tk.Tk()
    app.title("Бухгалтерия")
    app.geometry("1200x1400")
    app.configure(bg="#fcf0f8")  # Устанавливаем цвет фона для основного окна

    # Добро пожаловать
    tk.Label(
        app,
        text=f"Добро пожаловать, {current_user['username']}!",
        font=("Arial", 14),
        bg="#fcf0f8"
    ).pack(pady=10)

    # Кнопки
    tk.Button(
        app,
        text="Добавить расход",
        font=("Arial", 12),
        command=add_expense,
        bg="#fcf0f8"
    ).pack(pady=10)

    tk.Button(
        app,
        text="Добавить категорию",
        font=("Arial", 12),
        command=add_category,
        bg="#fcf0f8"
    ).pack(pady=10)

    tk.Button(
        app,
        text="Посмотреть отчет",
        font=("Arial", 12),
        command=view_reports,
        bg="#fcf0f8"
    ).pack(pady=10)

    tk.Button(
        app,
        text="Редактировать расход",
        font=("Arial", 12),
        command=edit_expense,
        bg="#fcf0f8"
    ).pack(pady=10)

    tk.Button(
        app,
        text="Удалить расход",
        font=("Arial", 12),
        command=delete_expense,
        bg="#fcf0f8"
    ).pack(pady=10)

    # Дерево расходов
    columns = ("ID", "Категория", "Сумма", "Дата", "Описание")
    global expense_tree
    expense_tree = ttk.Treeview(
        app,
        columns=columns,
        show="headings",
        height=15
    )

    for col in columns:
        expense_tree.heading(col, text=col)

    expense_tree.pack(fill="both", expand=True, pady=10)

    load_expenses()

    app.mainloop()


# Окно входа
login_window = tk.Tk()
login_window.title("Вход в систему")
login_window.geometry("500x300")
login_window.configure(bg="#fcf0f8")

# Метка для логина
tk.Label(
    login_window,
    text="Логин:",
    font=("Arial", 12),
    bg="#fcf0f8"
).pack(pady=5)

# Поле ввода для логина
login_username_entry = tk.Entry(login_window, font=("Arial", 12), bg="#fcf0f8")
login_username_entry.pack(pady=5)

# Метка для пароля
tk.Label(
    login_window,
    text="Пароль:",
    font=("Arial", 12),
    bg="#fcf0f8"
).pack(pady=5)

# Поле ввода для пароля
login_password_entry = tk.Entry(login_window, show="*", font=("Arial", 12), bg="#fcf0f8")
login_password_entry.pack(pady=5)

# Кнопка входа
tk.Button(
    login_window,
    text="Войти",
    font=("Arial", 12),
    command=login_user,
    bg="#fcf0f8"
).pack(pady=10)

# Кнопка регистрации
tk.Button(
    login_window,
    text="Регистрация",
    font=("Arial", 12),
    command=register_user,
    bg="#fcf0f8"
).pack(pady=10)

login_window.mainloop()

