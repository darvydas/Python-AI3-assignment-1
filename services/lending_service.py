import datetime
from services.library_service import LibraryService
from models.book import Book
from models.reader import Reader

class LendingService:
  def __init__(self):
    self.borrowed_books = {}  # Dictionary to store borrowed books

  def borrow_book(self, reader:Reader, book:Book, due_date):
    if book.available > 0:
      if self.check_overdue_status(reader):
        return None # reader has books due

      book.available -= 1
      reader.borrowed_books.append(book)

      # Store book title, due date, and reader ID
      if book.title not in self.borrowed_books:
        self.borrowed_books[book] = []
      self.borrowed_books[book].append({'due_date': due_date, 'reader_id': reader.id})

      print (self.borrowed_books)

      return True # Book is borrowed
    else:
      return False # Book is unavailable

  def return_book(self, reader:Reader, book:Book):
    print(reader)
    print(book)
    print(reader.borrowed_books)
    if book in reader.borrowed_books:
        book.available += 1
        reader.borrowed_books.remove(book)

        # Remove the book from borrowed_books
        if book in self.borrowed_books:
          self.borrowed_books[book] = [
            borrow_info for borrow_info in self.borrowed_books[book] if borrow_info['reader_id'] != reader.id
          ]
          if not self.borrowed_books[book]:
            del self.borrowed_books[book]

        print(f"{reader.name} has returned '{book.title}'.")
    else:
        print(f"{reader.name} has not borrowed '{book.title}'.")

  # def get_overdue_books(self):
  #   overdue_books = []
  #   today = datetime.date.today()
  #   for book, borrow_info_list in self.borrowed_books.items():
  #     for borrow_info in borrow_info_list:
  #       if borrow_info['due_date'] < today:
  #         overdue_books.append(book)
  #   return overdue_books
  #   return filter(lambda x: x for book, borrow_info_list in x, self.borrowed_books.items())

  def get_overdue_books(self):
    """Returns a list of overdue books."""
    today = datetime.date.today()
    overdue_books = {
      book: borrow_info_list \
      for book, borrow_info_list in self.borrowed_books.items() \
      if any(borrow_info['due_date'] < today for borrow_info in borrow_info_list)
    }
    print (overdue_books)
    return overdue_books

  def get_borrowed_books(self):
    ''' Returns borrowed books sorted by first reader due date. '''
    # borrowed_books = []
    # for book, borrow_info_list in self.borrowed_books.items():
    #   for borrow_info in borrow_info_list:
    #     # Create a copy of the book object to avoid modifying the original
    #     book_copy = Book(book.title, book.author, book.publication_year, book.genre)
    #     book_copy.due_date = borrow_info['due_date']  # Add the due_date attribute to the copy
    #     borrowed_books.append(book_copy)

    # # Sort by due_date
    # borrowed_books.sort(key=lambda x: x.due_date)
    # return borrowed_books
    # print( list(sorted(self.borrowed_books.items(), key=lambda item: item[1][0]['due_date'])) )
    return dict(sorted(self.borrowed_books.items(), key=lambda item: item[1][0]['due_date']))

  def check_overdue_status(self, reader:Reader):
      overdue_books = self.get_overdue_books()
      for book in overdue_books:
          if book in reader.borrowed_books:
              print(f"WARNING: '{book.title}' is overdue!")
              return book
      return None

  def get_reader_overdue_books(self, reader: Reader):
    """ Checks if a reader has any overdue books and returns a list of overdue books. """
    overdue_books = self.get_overdue_books()
    reader_overdue_books = []
    for book in overdue_books:
      if book in reader.borrowed_books:
        reader_overdue_books.append(book)
    return reader_overdue_books if reader_overdue_books else None