# main.py

from models.reader import Reader
from services.library_service import LibraryService
from services.lending_service import LendingService
from views import library_view, menu_view
import datetime

def get_publication_year():
  """Prompts the user for a publication year until a valid integer is entered."""
  while True:
    try:
      publication_year = int(input("Enter publication year: "))
      if 0 < publication_year < datetime.date.today().year:
        return publication_year  # Return the valid year
      print(f"Invalid publication year. Please enter a number from 0 to {datetime.date.today().year}.")
    except ValueError:
      print(f"Invalid publication year.")

def insert_new_book():
  """Gets book details from the user."""
  title = input("Enter title: ")
  author = input("Enter author: ")
  publication_year = get_publication_year()  # Call the function to get the year
  genre = input("Enter genre: ")

  return title, author, publication_year, genre  # Return all inputs


def main():
  library_service = LibraryService()
  lending_service = LendingService()

  while True:

    menu_view.display_menu()

    choice = input("Enter your choice: ")

    if choice == '1':
      title, author, publication_year, genre = insert_new_book()

      library_service.add_book(title, author, publication_year, genre)
      print("Book added successfully!") # was book already in store??

    elif choice == '2': # TODO: could remove by year or select a book from list
      title = input("Enter title of book to remove: ")
      removed_book = library_service.remove_book(title)
      if removed_book:
        print(f"Book \"{removed_book.title}\" by {removed_book.author} removed from library!")
      else:
        print("Book not found.")

    elif choice == '3':
      query = input("Enter title or author to search: ")
      results = library_service.find_book_by_title_or_author(query)
      library_view.display_search_results(results)

    elif choice == '4':
      library_view.display_all_books(library_service.books)

    elif choice == '5':
      reader_id = input("Enter reader ID: ")
      # TODO: should not create new reader object, check if already exists
      reader = Reader("Unknown", reader_id)  # Assuming reader name is not important for borrowing
      title = input("Enter title of book to borrow: ")
      book = library_service.get_book_by_title(title)
      if book:
        try:
          due_date_str = input("Enter due date (YYYY-MM-DD): ")
          due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
          # match lending_service.borrow_book(reader, book, due_date):
          #   case True:
          #     pass
          #   case None:
          #     pass
          #   case False:
          #     pass
          if not lending_service.check_overdue_status(reader):
            if lending_service.borrow_book(reader, book, due_date):
              print(f"{reader.name} has borrowed '{book.title}'. Due date: {due_date.strftime('%Y-%m-%d')}") # TODO: move print to views
            else:
              print(f"'{book.title}' is currently unavailable.")
          else:
            print(f"Reader {reader.name} has overdue books and cannot borrow more.")
            # TODO: print overdue books?
            # lending_service.get_reader_overdue_books()
        except ValueError:
          print("Invalid date format. Please use YYYY-MM-DD.")
      else:
        print("Book not found.")

    elif choice == '6':
        reader_id = input("Enter reader ID: ")
        # reader = Reader("Unknown", reader_id)
        # TODO: check if reader_id is valid

        title = input("Enter title of book to return: ")
        book = library_service.get_book_by_title(title)
        if book:
            lending_service.return_book(reader, book)
        else:
            print("Book not found.")

    elif choice == '7':
        overdue_books = lending_service.get_overdue_books()
        library_view.display_overdue_books(overdue_books)  # Use the view function
        # TODO: should print overdue date

    elif choice == '8':
        borrowed_books = lending_service.get_borrowed_books()
        library_view.display_borrowed_books(borrowed_books)  # Use the view function

    elif choice == '9':
        print("Exiting Library Management System.")
        break

    elif choice == '10':
        library_service.add_book('Untouched book', 'Mr. B', 2000, 'Fiction')
        library_service.add_book('Banana book', 'Mr. B', 2000, 'Fiction') # borrowed and not due
        library_service.add_book('Banana book2', 'Mr. B', 2010, 'Fiction') # borrowed and overdue
        library_service.add_book('Banana book3', 'Mr. B', 2010, 'Fiction') # not borrowed because overdue

        reader = Reader("Dummy data", 'dreader')
        book = library_service.get_book_by_title('Banana book')
        lending_service.borrow_book(reader, book, datetime.datetime.strptime('2025-01-01', "%Y-%m-%d").date()) # not due

        book = library_service.get_book_by_title('Banana book2')
        lending_service.borrow_book(reader, book, datetime.datetime.strptime('2024-12-01', "%Y-%m-%d").date()) # overdue

        book = library_service.get_book_by_title('Banana book3')
        lending_service.borrow_book(reader, book, datetime.datetime.strptime('2025-01-01', "%Y-%m-%d").date()) # not due


    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
  main()
