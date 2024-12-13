class Reader:
    def __init__(self, name, reader_id):
        self.name = name
        self.id = reader_id
        self.borrowed_books = []
        self._card_id = ""

    def __str__(self):
        return f"Reader ID: {self.id}\nName: {self.name}\nCard ID: {self._card_id}\nBorrowed books: {', '.join([book.title for book in self.borrowed_books]) if self.borrowed_books else 'None'}"

    def get_reader_card(self):
        return self._card_id if self._card_id else None

    def set_reader_card(self, reader_card_id):
        self._card_id = reader_card_id
