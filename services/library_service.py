from models.book import Book

class LibraryService:
    def __init__(self):
        self.books:list[Book] = []

    def add_book(self, title, author, publication_year, genre):
      book = Book(title, author, publication_year, genre)
      self.books.append(book)

    def remove_book(self, title):
      for book in self.books:
        if book.title == title:
          self.books.remove(book)
          return book
      else:
        return None


    def find_book(self, query):
        results = []
        for book in self.books:
            if query.lower() in book.title.lower() or query.lower() in book.author.lower():
                results.append(book)
        return results

    def display_all_books(self):
        for book in self.books:
            print(book)
            print("---")