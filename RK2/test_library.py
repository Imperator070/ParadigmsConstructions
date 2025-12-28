import unittest
import sqlite3
from library import (
    create_tables,
    insert_data,
    query_1,
    query_2,
    query_3
)

class TestLibraryQueries(unittest.TestCase):
    
    def setUp(self):
        """Создаем in-memory базу данных перед каждым тестом"""
        self.conn = sqlite3.connect(':memory:')
        create_tables(self.conn)
        insert_data(self.conn)
    
    def tearDown(self):
        """Закрываем соединение после каждого теста"""
        self.conn.close()
    
    def test_query_1_returns_correct_authors(self):
        """Проверяем, что запрос 1 возвращает правильных авторов"""
        result = query_1(self.conn)
        
        # Ожидаемые результаты (авторы с книгами 1900-2000 гг)
        expected = [
            ('Маркес',),
            ('Оруэлл',),
            ('Хемингуэй',)
        ]
        
        self.assertEqual(result, expected)
    
    def test_query_2_returns_current_issues(self):
        """Проверяем, что запрос 2 возвращает книги на руках"""
        result = query_2(self.conn)
        
        # Ожидаемые результаты (название, автор)
        expected = [
            ('Анна Каренина', 'Толстой'),
            ('Идиот', 'Достоевский'),
            ('Преступление и наказание', 'Достоевский'),
            ('Сто лет одиночества', 'Маркес')
        ]
        
        self.assertEqual(result, expected)
    
    def test_query_3_counts_books_correctly(self):
        """Проверяем, что запрос 3 правильно считает книги"""
        result = query_3(self.conn)
        
        # Ожидаемые результаты (фамилия, количество)
        expected = {
            'Иванов': 2,
            'Петров': 2,
            'Сидорова': 2,
            'Кузнецов': 1
        }
        
        # Проверяем соответствие данных
        self.assertEqual(len(result), 4)
        for surname, count in result:
            self.assertEqual(count, expected[surname])

if __name__ == '__main__':
    unittest.main()