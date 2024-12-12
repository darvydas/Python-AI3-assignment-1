# main.py

from models.reader import Reader
from services.library_service import LibraryService
from services.lending_service import LendingService
from services.pickle_service import save_to_pickle, load_from_pickle
from views import library_view, menu_view
import datetime
import constants as const

def input_publication_year():
  """Prompts the user for a publication year until a valid integer is entered."""
  while True:
    try:
      publication_year = int(input("Enter publication year (YYYY): "))
      if 0 < publication_year < datetime.date.today().year:
        return publication_year  # Return the valid year
      menu_view.display_error_msg(f"Invalid publication year. Please enter a number from 0 to {datetime.date.today().year}.")
    except ValueError:
      menu_view.display_error_msg(f"Invalid publication year.")

def insert_new_book():
  """Gets book details from the user."""
  title = input("Enter title: ")
  author = input("Enter author: ")
  publication_year = input_publication_year()  # Call the function to get the year
  genre = input("Enter genre: ")

  return title, author, publication_year, genre  # Return all inputs

def get_book_by_title_input(library_service:LibraryService): #TODO: might result in infinite loop if book name is not known
  """Gets a book by title from user input."""
  while True:
    title = input("Enter title of book: ")
    book = library_service.get_book_by_title(title)
    if not book:
      menu_view.display_error_msg("Book not found. Please try again.")
      # TODO: ask to leave input? or skip if failed?
      continue
    return book

def input_due_date():
  """Gets a due date from user input."""
  while True:
    try:
      due_date_str = input("Enter due date (YYYY-MM-DD): ")
      due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
      return due_date
    except ValueError:
      menu_view.display_error_msg("Invalid date format. Please use YYYY-MM-DD.")

def main():
  library_service = LibraryService()
  lending_service = LendingService()

  load_from_pickle(const.LIBRARY_DATA_FILENAME, library_service, lending_service)

  while True:

    menu_view.display_menu()

    choice = input("Enter your choice: ")

    if choice == '1':
      title, author, publication_year, genre = insert_new_book()

      library_service.add_book(title, author, publication_year, genre) # TODO: should return added book
      menu_view.display_success_msg("Book added successfully!")

    elif choice == '2': # TODO: could remove by year or select a book from list
      title = input("Enter title of book to remove: ")
      removed_book = library_service.remove_book(title)
      if removed_book:
        menu_view.display_success_msg(f"Book \"{removed_book.title}\" by {removed_book.author} removed from library!")
      else:
        menu_view.display_error_msg("Book not found.")

    elif choice == '3':
      query = input("Enter title or author to search: ")
      results = library_service.find_book_by_title_or_author(query)
      library_view.display_search_results(results)

    elif choice == '4':
      library_view.display_all_books(library_service.books)

    elif choice == '5':
      reader_id = input("Enter reader ID: ")
      reader:Reader = lending_service.get_or_create_reader(reader_id)
      if lending_service.check_overdue_status(reader):
        menu_view.display_error_msg(f"Reader {reader.name} has overdue books and cannot borrow more.")
        overdue_books = lending_service.get_reader_overdue_books(reader)
        library_view.display_overdue_books(overdue_books)
        continue  # Move back to the menu

      book = get_book_by_title_input(library_service)
      if not book.available > 0:
        menu_view.display_error_msg(f"Book {book.title} is out of stock.")
        continue

      due_date = input_due_date()

      if lending_service.borrow_book(reader, book, due_date):
        menu_view.display_success_msg(f"{reader.name} has borrowed '{book.title}'. Due date: {due_date.strftime('%Y-%m-%d')}")
      else:
        menu_view.display_error_msg(f"Book {book.title} is unavailable.")

    elif choice == '6':
      reader_id = input("Enter reader ID: ")

      if not reader_id.isalnum():
        menu_view.display_error_msg(f'Ivalid reader ID: {reader_id}. Please use numbers and letters only.')
        continue

      reader = lending_service.get_reader(reader_id)  # Get the reader, if exists

      if not reader:  # Check if the reader exists
        menu_view.display_error_msg(f'There is no reader with ID: {reader_id}.')

      book = get_book_by_title_input(library_service)
      # if not book: # this is already done on get_book_by_title_input
      #   print("Book not found.")

      if lending_service.return_book(reader, book):
        menu_view.display_success_msg(f"{reader.name} has returned '{book.title}'.")
      else:
        menu_view.display_error_msg(f"{reader.name} has not borrowed '{book.title}'.")

    elif choice == '7':
      overdue_books = lending_service.get_overdue_books()
      library_view.display_overdue_books(overdue_books)  # Use the view function

    elif choice == '8':
      borrowed_books = lending_service.get_borrowed_books()
      library_view.display_borrowed_books(borrowed_books)  # Use the view function

    elif choice == '9':
      save_to_pickle(const.LIBRARY_DATA_FILENAME, library_service, lending_service) #TODO: could save on every data change
      menu_view.display_system_msg("Exiting Library Management System.")
      break

    elif choice == '10':
      library_service.add_book('Untouched book', 'Mr. B', 2000, 'Fiction')
      library_service.add_book('Banana book', 'Mr. B', 2000, 'Fiction') # borrowed and not due
      library_service.add_book('Banana book2', 'Mr. B', 2010, 'Fiction') # borrowed and overdue
      library_service.add_book('Banana book3', 'Mr. B', 2010, 'Fiction') # not borrowed because overdue

      reader = lending_service.get_or_create_reader('dreader',"Dummy data")
      book = library_service.get_book_by_title('Banana book')
      lending_service.borrow_book(reader, book, datetime.datetime.strptime('2025-01-01', "%Y-%m-%d").date()) # not due

      book = library_service.get_book_by_title('Banana book2')
      lending_service.borrow_book(reader, book, datetime.datetime.strptime('2024-12-01', "%Y-%m-%d").date()) # overdue

      book = library_service.get_book_by_title('Banana book3')
      lending_service.borrow_book(reader, book, datetime.datetime.strptime('2025-01-01', "%Y-%m-%d").date()) # not due


    else:
      menu_view.display_error_msg("Invalid menu choice. Please try again.")

if __name__ == "__main__":
  main()
