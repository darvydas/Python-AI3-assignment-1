# views/library_view.py
from models.book import Book

def display_book(book:Book, due_date = None, card_id = ''):
  """Displays details of a single book."""
  if card_id and due_date:
    print(f"| {card_id:<10} | {str(due_date):<10} | {book.title:<30} | {book.author:<20} | {book.publication_year:<5} | {book.genre:<15} | {book._available:<5} | ")
  else:
    print(f"| {book.title:<30} | {book.author:<20} | {book.publication_year:<5} | {book.genre:<15} | {book._available:<5} |")

def display_all_books(books):
  """Displays details of all books in the library."""
  if books:
    print("-"*91)
    print(f"| {'Title:':<30} | {'Author:':<20} | {'Year:':<5} | {'Genre':<15} | {'Stock':<5} |")
    print("-"*91)
    for book in books:
      display_book(book)
    print("-"*91)
  else:
    print("No books in the library yet.")

def display_search_results(results):
  """Displays sea
  rch results for books."""
  if results:
    print("-"*91)
    print(f"| {'Title:':<30} | {'Author:':<20} | {'Year:':<5} | {'Genre':<15} | {'Stock':<5} |")
    print("-"*91)
    for book in results:
      display_book(book)
    print("-"*91)
  else:
    print("No books found matching your query.")

def display_overdue_books(overdue_books):
  """Displays details of overdue books."""
  if overdue_books:
    print("\n"+"-"*117)
    print("Overdue books:")
    print("-"*117)
    print(f"| {'Card ID:':<10} | {'Due date:':<10} | {'Title:':<30} | {'Author:':<20} | {'Year':<5} | {'Genre':<15} | {'Stock':<5} |")
    print("-"*117)
    for book, borrow_info_list in overdue_books.items():
      for borrow_info in borrow_info_list:
        display_book(book, borrow_info['due_date'], borrow_info['card_id'])
    print("-"*117)
  else:
    print("No overdue books.")

def display_borrowed_books (borrowed_books):
  """Displays details of borrowed books."""
  if borrowed_books:
    print("\n"+"-"*117)
    print("Borrowed books:")
    print("-"*117)
    print(f"| {'Card ID:':<10} | {'Due date:':<10} | {'Title:':<30} | {'Author:':<20} | {'Year':<5} | {'Genre':<15} | {'Stock':<5} |")
    print("-"*117)
    # for book in borrowed_books:
    #   display_book(book)
    for book, borrow_info_list in borrowed_books.items():
      for borrow_info in borrow_info_list:
        display_book(book, borrow_info['due_date'], borrow_info['card_id'])
    print("-"*117)
  else:
    print("No borrowed books.")
