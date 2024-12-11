from models.book import Book

class LibraryService:
  def __init__(self):
    self.books:list[Book] = []

  def add_book(self, title, author, publication_year, genre):
    # TODO: should check if book is already in list and increase book.available count
    book = Book(title, author, publication_year, genre)
    self.books.append(book)

  def remove_book(self, title):
    for book in self.books:
      if book.title == title:
        self.books.remove(book)
        return book
    else:
      return None

  def get_book_by_title(self, book_title):
    return next((book for book in self.books if book.title == book_title), None)

  def find_book_by_title_or_author(self, query):
    results = []
    for book in self.books:
      if query.lower() in book.title.lower() or query.lower() in book.author.lower():
        results.append(book)
    return results