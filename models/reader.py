class Reader:
    def __init__(self, name, reader_id):
        self.name = name
        self.id = reader_id
        self.borrowed_books = []

    def __str__(self):
        return f"Reader ID: {self.id}\nName: {self.name}\nBorrowed books: {', '.join([book.title for book in self.borrowed_books]) if self.borrowed_books else 'None'}"