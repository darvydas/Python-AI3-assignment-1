class Book:
    def __init__(self, title, author, publication_year, genre):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre
        self._available = 1

    def increase_available(self, quantity=1):
        self._available += quantity

    def decrease_available(self, quantity=1):
        self._available -= quantity

    def is_available(self) -> bool:
        """Checks if the book is currently available."""
        return self._available > 0

    def __str__(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nPublication Year: {self.publication_year}\nGenre: {self.genre}\nAvailable: {self._available}"