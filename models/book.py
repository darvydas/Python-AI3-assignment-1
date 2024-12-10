class Book:
    def __init__(self, title, author, publication_year, genre):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre
        self.available = 1

    def __str__(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nPublication Year: {self.publication_year}\nGenre: {self.genre}\nAvailable: {self.available}"