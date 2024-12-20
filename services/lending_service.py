import datetime
from services.library_service import LibraryService
from models.book import Book
from models.reader import Reader

class LendingService:
  def __init__(self, borrowed_books = {}):
    self.borrowed_books = borrowed_books  # Dictionary to store borrowed books

  def borrow_book(self, reader:Reader, book:Book, due_date):
    if book.is_available():
      if self.check_overdue_status(reader):
        return None # reader has books due

      book.decrease_available()
      reader.borrowed_books.append(book)

      # Store book title, due date, and reader ID
      if book.title not in self.borrowed_books:
        self.borrowed_books[book] = []
      self.borrowed_books[book].append({'due_date': due_date, 'card_id': reader.get_reader_card_id()})

      return True # Book is borrowed
    else:
      return False # Book is unavailable

  def return_book(self, reader:Reader, book:Book):
    if book in reader.borrowed_books:
      book.increase_available()
      reader.borrowed_books.remove(book)

      # Remove the book from borrowed_books
      if book in self.borrowed_books:
        self.borrowed_books[book] = [
          borrow_info for borrow_info in self.borrowed_books[book] if borrow_info['card_id'] != reader.get_reader_card_id()
        ]
        if not self.borrowed_books[book]:
          del self.borrowed_books[book]

        return book

  # def get_overdue_books(self):
  #   overdue_books = []
  #   today = datetime.date.today()
  #   for book, borrow_info_list in self.borrowed_books.items():
  #     for borrow_info in borrow_info_list:
  #       if borrow_info['due_date'] < today:
  #         overdue_books.append(book)
  #   return overdue_books

  def get_overdue_books(self):
    """Returns a list of overdue books."""
    today = datetime.date.today()
    overdue_books = {
      book: borrow_info_list \
      for book, borrow_info_list in self.borrowed_books.items() \
      if any(borrow_info['due_date'] < today for borrow_info in borrow_info_list)
    }
    return overdue_books

  def get_borrowed_books(self, reader:Reader = None):
    ''' Returns borrowed books sorted by first reader due date. '''
    if reader:
      borrowed_books = {}
      for book, borrow_info_list in self.borrowed_books.items():
        for borrow_info in borrow_info_list:
          if borrow_info['card_id'] == reader.get_reader_card_id():
            borrowed_books[book] = []
            borrowed_books[book].append(borrow_info)

      return dict(sorted(borrowed_books.items(), key=lambda item: item[1][0]['due_date']))
    else:
      return dict(sorted(self.borrowed_books.items(), key=lambda item: item[1][0]['due_date'])) #TODO: could sort by all reader due_date first

  def check_overdue_status(self, reader:Reader):
      overdue_books = self.get_overdue_books()
      for book in overdue_books:
          if book in reader.borrowed_books:
              # print(f"WARNING: '{book.title}' is overdue!")
              return True
      return False

  def get_reader_overdue_books(self, reader: Reader):
    """ Checks if a reader has any overdue books and returns a list of overdue books. """
    overdue_books = self.get_overdue_books()

    reader_overdue_books = {}
    for book, borrow_info_list in overdue_books.items():
      if book in reader.borrowed_books:
        reader_overdue_books[book] = []
        for borrow_info in borrow_info_list:
          if borrow_info['card_id'] == reader.id:
            reader_overdue_books[book].append(borrow_info)
    return reader_overdue_books if reader_overdue_books else None
