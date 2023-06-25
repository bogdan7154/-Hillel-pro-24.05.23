import sqlite3
import unittest
from unittest.mock import patch
from bank_card_model.card import BankCard


class BankCardTests(unittest.TestCase):
    def setUp(self):
        # Підготовка до тестування
        self.card = BankCard("1234567812345678", "06/25", "123", "2023-06-21", "b10a5c46-ef20-4f6e-a52c-68b28e8c5d43", "нова")
        self.card.save_to_database()

    def tearDown(self):
        # Очищення після тестування
        conn = sqlite3.connect('../bank_cards.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bank_cards')
        conn.commit()
        conn.close()

    def test_activate_valid_status(self):
        # Переконуємося, що картка активується, якщо статус "нова"
        self.assertTrue(self.card.activate())
        self.assertEqual(self.card.status, "активна")

    def test_activate_already_active(self):
        # Переконуємося, що картка не активується, якщо статус вже "активна"
        self.card.status = "активна"
        self.assertFalse(self.card.activate())
        self.assertEqual(self.card.status, "активна")

    def test_block_valid_status(self):
        # Переконуємося, що картка блокується, якщо статус не "заблокована"
        self.assertTrue(self.card.block())
        self.assertEqual(self.card.status, "заблокована")

    def test_block_already_blocked(self):
        # Переконуємося, що картка не блокується, якщо статус вже "заблокована"
        self.card.status = "заблокована"
        self.assertFalse(self.card.block())
        self.assertEqual(self.card.status, "заблокована")

    @patch('bank_card.sqlite3.connect')
    def test_save_to_database(self, mock_connect):
        # Переконуємося, що дані картки зберігаються в базі даних
        mock_cursor = mock_connect.return_value.cursor.return_value
        self.card.save_to_database()
        mock_cursor.execute.assert_called_once_with(
            'INSERT INTO bank_cards VALUES (?, ?, ?, ?, ?, ?)',
            ("1234567812345678", "06/25", "123", "2023-06-21", "b10a5c46-ef20-4f6e-a52c-68b28e8c5d43", "нова")
        )

    @patch('bank_card.sqlite3.connect')
    def test_read_from_database(self, mock_connect):
        # Переконуємося, що дані карток читаються з бази даних
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [("1234567812345678", "06/25", "123", "2023-06-21", "b10a5c46-ef20-4f6e-a52c-68b28e8c5d43", "нова")]
        cards = BankCard.read_from_database()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM bank_cards')
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0].pan, "1234567812345678")
        self.assertEqual(cards[0].expiration_date, "06/25")
        self.assertEqual(cards[0].cvv, "123")
        self.assertEqual(cards[0].issue_date, "2023-06-21")
        self.assertEqual(cards[0].owner_id, "b10a5c46-ef20-4f6e-a52c-68b28e8c5d43")
        self.assertEqual(cards[0].status, "нова")


if __name__ == '__main__':
    unittest.main()
