import pytest
from unittest.mock import MagicMock, patch
import app7MAIN  # Имя основного файла приложения
from app7MAIN import connect_to_db, get_categories, add_expense

@pytest.fixture
def mock_db():
    """Фикстура для имитации подключения к базе данных."""
    with patch("mysql.connector.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        yield mock_conn

def test_connect_to_db_success(mock_db):
    """Проверка успешного подключения к базе данных."""
    conn = connect_to_db()
    assert conn is not None


def test_get_categories(mock_db):
    """Проверка получения списка категорий из базы данных."""
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchall.return_value = [("Еда",), ("Развлечения",)]
    categories = get_categories()
    assert categories == ["Еда", "Развлечения"]