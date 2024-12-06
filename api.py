from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Конфигурация базы данных
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Имя пользователя MySQL
    'password': 'admin',  # Пароль для базы
    'database': 'buhgalteria'  # Название базы данных
}

def connect_to_db():
    """Подключение к базе данных."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        return None

# Получение списка записей (GET)
@app.route('/expenses', methods=['GET'])
@app.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expenses(expense_id=None):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)

            # Если был передан expense_id, ищем конкретный расход
            if expense_id:
                cursor.execute(
                    """
                    SELECT e.expense_id, c.category_name, e.amount, e.expense_date, e.description_
                    FROM expenses e
                    JOIN categories c ON e.category_id = c.category_id
                    WHERE e.expense_id = %s
                    """, (expense_id,)
                )
                expense = cursor.fetchone()  # Получаем одну запись
                if expense:
                    return jsonify(expense)
                else:
                    return jsonify({'error': 'Расход с таким ID не найден'}), 404
            else:
                # Если expense_id не передан, возвращаем все расходы
                cursor.execute(
                    """
                    SELECT e.expense_id, c.category_name, e.amount, e.expense_date, e.description_
                    FROM expenses e
                    JOIN categories c ON e.category_id = c.category_id
                    """
                )
                expenses = cursor.fetchall()
                return jsonify(expenses)

        except mysql.connector.Error as e:
            return jsonify({'error': str(e)})
        finally:
            conn.close()
    return jsonify({'error': 'Не удалось подключиться к базе данных'})


# Добавление новой записи (POST)
@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json
    category_name = data.get('category_name')
    amount = data.get('amount')
    expense_date = data.get('expense_date')
    description = data.get('description_')
    user_id = data.get('user_id')

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO expenses (category_id, amount, expense_date, description_, user_id)
                VALUES (
                    (SELECT category_id FROM categories WHERE category_name = %s),
                    %s, %s, %s, %s
                )
                """, (category_name, amount, expense_date, description, user_id)
            )
            conn.commit()
            return jsonify({'message': 'Расход добавлен успешно'}), 201
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)})
        finally:
            conn.close()
    return jsonify({'error': 'Не удалось подключиться к базе данных'})

# Обновление записи (PUT)
@app.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.json
    category_name = data.get('category_name')
    amount = data.get('amount')
    expense_date = data.get('expense_date')
    description = data.get('description_')

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
                """, (category_name, amount, expense_date, description, expense_id)
            )
            conn.commit()
            return jsonify({'message': 'Расход обновлен успешно'})
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)})
        finally:
            conn.close()
    return jsonify({'error': 'Не удалось подключиться к базе данных'})

# Удаление записи (DELETE)
@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE expense_id = %s", (expense_id,))
            conn.commit()
            return jsonify({'message': 'Расход удален успешно'})
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)})
        finally:
            conn.close()
    return jsonify({'error': 'Не удалось подключиться к базе данных'})

if __name__ == '__main__':
    app.run(debug=True)
