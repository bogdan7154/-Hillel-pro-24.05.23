import sqlite3
import uuid


class BankCard:
    def __init__(self, pan, expiration_date, cvv, issue_date, owner_id, status):
        self.pan = pan
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.issue_date = issue_date
        self.owner_id = owner_id
        self.status = status

    def activate(self):
        if self.status == 'нова':
            self.status = 'активна'
            return True
        return False

    def block(self):
        if self.status != 'заблокована':
            self.status = 'заблокована'
            return True
        return False

    def save_to_database(self):
        conn = sqlite3.connect('../bank_cards.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS bank_cards
                          (pan TEXT, expiration_date TEXT, cvv TEXT,
                           issue_date TEXT, owner_id TEXT, status TEXT)''')
        cursor.execute('INSERT INTO bank_cards VALUES (?, ?, ?, ?, ?, ?)',
                       (self.pan, self.expiration_date, self.cvv, self.issue_date, self.owner_id, self.status))
        conn.commit()
        conn.close()

    @staticmethod
    def read_from_database():
        conn = sqlite3.connect('../bank_cards.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bank_cards')
        rows = cursor.fetchall()
        conn.close()
        cards = []
        for row in rows:
            card = BankCard(row[0], row[1], row[2], row[3], row[4], row[5])
            cards.append(card)
        return cards
