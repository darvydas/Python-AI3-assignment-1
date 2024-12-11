# views/library_view.py

def display_book(book, due_date = None, reader_id = ''):
  """Displays details of a single book."""
  if reader_id:
    print(f"Reader ID: {reader_id}")
  if due_date:
    print(f"Due date: {due_date}")
  print(book)
  print("---")

def display_all_books(books):
  """Displays details of all books in the library."""
  if books:
    for book in books:
      display_book(book)
  else:
    print("No books in the library yet.")

def display_search_results(results):
  """Displays search results for books."""
  if results:
    for book in results:
      display_book(book)
  else:
    print("No books found matching your query.")

def display_overdue_books(overdue_books):
  """Displays details of overdue books."""
  if overdue_books:
    print("\nOverdue books:")
    for book, borrow_info_list in overdue_books.items():
      for borrow_info in borrow_info_list:
        display_book(book, borrow_info['due_date'], borrow_info['reader_id'])
  else:
    print("No overdue books.")

def display_borrowed_books (borrowed_books):
  """Displays details of borrowed books."""
  if borrowed_books:
    print("\nBorrowed books:")
    # for book in borrowed_books:
    #   display_book(book)
    for book, borrow_info_list in borrowed_books.items():
      for borrow_info in borrow_info_list:
        display_book(book, borrow_info['due_date'], borrow_info['reader_id'])
  else:
    print("No borrowed books.")