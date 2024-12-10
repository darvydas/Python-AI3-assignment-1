# views/library_view.py

def display_book(book):
  """Displays details of a single book."""
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