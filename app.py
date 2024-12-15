# main.py

from models.reader import Reader
from models.role import Role
from services.library_service import LibraryService
from services.lending_service import LendingService
from services.reader_service import ReaderService
from services.pickle_service import save_to_pickle, load_from_pickle
from services.login_service import AuthenticationService
from views import library_view, menu_view, system_view
import datetime
import constants as const
import traceback
import getpass

def input_publication_year():
  """Prompts the user for a publication year until a valid integer is entered."""
  while True:
    try:
      publication_year = int(input("Enter publication year (YYYY): ").strip())
      if 0 < publication_year < datetime.date.today().year:
        return publication_year  # Return the valid year
      menu_view.display_error_msg(f"Invalid publication year. Please enter a number from 0 to {datetime.date.today().year}.")
    except ValueError:
      menu_view.display_error_msg(f"Invalid publication year.")

def insert_new_book():
  """Gets book details from the user."""
  title = input("Enter title: ").strip()
  author = input("Enter author: ").strip()
  publication_year = input_publication_year()  # Call the function to get the year
  genre = input("Enter genre: ").strip()

  return title, author, publication_year, genre  # Return all inputs

def get_book_by_title_input(library_service:LibraryService):
  """Gets a book by title from user input."""
  while True:
    title = input("Enter title of book: ").strip()
    book = library_service.get_book_by_title(title)
    if not book:
      menu_view.display_error_msg("Book not found.")

      yes_no = input("Do you want to enter another one? (yes / y): ").strip()
      if yes_no not in ['yes','y']:
        break

      continue
    return book

def input_due_date():
  """Gets a due date from user input."""
  while True:
    try:
      due_date_str = input("Enter due date (YYYY-MM-DD): ").strip()
      due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
      return due_date
    except ValueError:
      menu_view.display_error_msg("Invalid date format. Please use YYYY-MM-DD.")

def input_username():
  while True:
    username = input("Enter username: ").strip()

    if username.isalnum():
      return username
    else:
      menu_view.display_error_msg('Username should use letters and numbers only!')

def input_password(need_confirm = False):
  while True:
    password = getpass.getpass("Enter password: ").strip()

    if need_confirm:
      confirm_password = getpass.getpass("Confirm password: ")
      if password == confirm_password:
        return password
      else:
        menu_view.display_error_msg("Passwords do not match. Please try again.")
        continue

    return password


def user_login_input(auth_service:AuthenticationService):
  while True:
    menu_view.display_login_menu()

    choice = input("Choose how you want to login: ").strip()

    if choice == '1': # Librarian login: username & password
      menu_view.display_info_msg("You have chosen 1: Librarian login\n")
      try:
        username = input_username()
        password = input_password()

        user = auth_service.authenticate_librarian(username, password)
        if user:
          return user
        else:
          menu_view.display_error_msg("Invalid username or password.")
      except ValueError:
        menu_view.display_error_msg("Invalid input format for librarian login.")

    elif choice == '2': # Reader login: reader_card_id
      menu_view.display_info_msg("You have chosen 2: Reader card ID\n")
      reader_card_input = input("Enter your card ID): ") #TODO: finish checking valid reader card
      user = auth_service.validate_reader_card(reader_card_input)
      if user:
        return user
      else:
        menu_view.display_error_msg("Invalid reader card ID.")

    elif choice == '3': # Register new librarian
      menu_view.display_info_msg("You have chosen 3: Register new librarian\n")
      username = input_username()
      password = input_password(need_confirm=True)
      # while True:
      #     role_input = input("Enter role (1 for Librarian, 2 for Reader): ")
      #     if role_input == "1":
      #         role = Role.LIBRARIAN
      #         break
      #     elif role_input == "2":
      #         role = Role.READER
      #         break
      #     else:
      #         print("Invalid role selection. Please enter 1 or 2.")
      user = auth_service.register_librarian(username,password) # TODO: finish register
      if user:
        menu_view.display_success_msg(f"User {username} registered successfully as {user.role.value}!")
        continue
      else:
        menu_view.display_error_msg("Register failed.")



    else:
      menu_view.display_error_msg("Invalid menu choice. Please try again.")


def main():

  file_load, file_data = load_from_pickle(const.LIBRARY_DATA_FILENAME)

  if file_load is True:
    library_service = LibraryService(file_data['books'])
    lending_service = LendingService(file_data['borrowed_books'])
    reader_service = ReaderService(file_data['readers'], file_data['reader_card_nums'], file_data['reader_cards'])
    auth_service = AuthenticationService(file_data['users'])
    if const.ENVIRONMENT == 'dev':
      system_view.display_system_msg(f"Data loaded from {const.LIBRARY_DATA_FILENAME}")
  else:
    if const.ENVIRONMENT == 'dev':
      system_view.display_system_msg(f"Error: {file_data}")
    library_service = LibraryService()
    lending_service = LendingService()
    reader_service = ReaderService()
    auth_service = AuthenticationService()


  while True:
    try:
      if not auth_service.logged_in:
        user_login_input(auth_service)

        if not auth_service.logged_in:
          menu_view.display_error_msg('Failed to login!')
          continue
        else:
          menu_view.display_success_msg(f'You are logged in as: {auth_service.logged_in.username}')
      else:
        menu_view.display_info_msg(f'You are logged in as: {auth_service.logged_in.username}')

      menu_view.display_menu() # TODO: Skaitytojas negali pridėti/išimti knygų

      choice = input("Enter your choice: ").strip()

      if choice == '1': # Add book
        title, author, publication_year, genre = insert_new_book()
        if not all([title, author, publication_year, genre]):
          menu_view.display_error_msg("Book fields were left empty. Please try again.")
          continue

        book = library_service.add_book(title, author, publication_year, genre)
        menu_view.display_success_msg(f"Book '{book.title}' added successfully!") # TODO: notify user if it was already there?

      elif choice == '2': # Remove book
        title = input("Enter title of book to remove: ").strip()
        if not title:
          menu_view.display_error_msg("Uable to remove book without a name.")
          continue

        removed_book = library_service.remove_book(title)
        if removed_book:
          menu_view.display_success_msg(f"Book \"{removed_book.title}\" by {removed_book.author} removed from library!")
        else:
          menu_view.display_error_msg("Book not found.")

      elif choice == '3': # Find book
        query = input("Enter title or author to search: ").strip() # if search is empty -> look for all books
        results = library_service.find_book_by_title_or_author(query)
        library_view.display_search_results(results)

      elif choice == '4': # Display all books
        library_view.display_all_books(library_service.books)

      elif choice == '5': # Borrow book #TODO: Knygas galima pasiimti tik su skaitytoje kortele
        reader_id = input("Enter reader ID: ").strip()
        if not reader_id:
          menu_view.display_error_msg("Reader ID empty is not valid.")
          continue

        reader:Reader = reader_service.get_or_create_reader(reader_id)
        if lending_service.check_overdue_status(reader):
          menu_view.display_error_msg(f"Reader {reader.name} has overdue books and cannot borrow more.")
          overdue_books = lending_service.get_reader_overdue_books(reader)
          library_view.display_overdue_books(overdue_books)
          continue  # Move back to the menu

        book = get_book_by_title_input(library_service)
        if not book:
          continue
        if not book.is_available():
          menu_view.display_error_msg(f"Book {book.title} is out of stock.")
          continue

        due_date = input_due_date()

        if lending_service.borrow_book(reader, book, due_date):
          menu_view.display_success_msg(f"{reader.name} has borrowed '{book.title}'. Due date: {due_date.strftime('%Y-%m-%d')}")
        else:
          menu_view.display_error_msg(f"Book {book.title} is unavailable.")

      elif choice == '6': # Return book #TODO: Knygas galima grąžinti tik su skaitytoje kortele
        reader_id = input("Enter reader ID: ").strip()

        if not reader_id or not reader_id.isalnum():
          menu_view.display_error_msg(f'Ivalid reader ID: \'{reader_id}\'. Please use numbers and letters only.')
          continue

        reader = reader_service.get_reader(reader_id)  # Get the reader, if exists

        if not reader:  # Check if the reader exists
          menu_view.display_error_msg(f'There is no reader with ID: {reader_id}.')

        book = get_book_by_title_input(library_service)
        if not book:
          continue

        if lending_service.return_book(reader, book):
          menu_view.display_success_msg(f"{reader.name} has returned '{book.title}'.")
        else:
          menu_view.display_error_msg(f"{reader.name} has not borrowed '{book.title}'.")

      elif choice == '7': # View overdue books
        overdue_books = lending_service.get_overdue_books()
        library_view.display_overdue_books(overdue_books)  # Use the view function

      elif choice == '8': # View borrowed books
        borrowed_books = lending_service.get_borrowed_books()
        library_view.display_borrowed_books(borrowed_books)  # Use the view function

      elif choice == '9': # Exit
        reader_card_nums = reader_service.get_used_reader_card_numbers()
        file_save = save_to_pickle(const.LIBRARY_DATA_FILENAME, library_service.books, lending_service.borrowed_books, reader_service.readers, reader_card_nums, reader_service.reader_cards, auth_service.users)
        if const.ENVIRONMENT == 'dev':
          if file_save is True:
            system_view.display_system_msg(f"Data saved to {const.LIBRARY_DATA_FILENAME}")
          else:
            system_view.display_system_msg(f"Error: {file_save}")

        system_view.display_system_msg("\nExiting Library Management System.")
        break

      elif choice == '10': # Add dummy data
        library_service.add_book('Untouched book', 'Mr. B', 2000, 'Fiction')
        library_service.add_book('Banana book', 'Mr. B', 2000, 'Fiction') # borrowed and not due
        library_service.add_book('Banana book2', 'Mr. B', 2010, 'Fiction') # borrowed and overdue
        library_service.add_book('Banana book3', 'Mr. B', 2010, 'Fiction') # not borrowed because overdue

        reader = reader_service.get_or_create_reader('dreader',"Dummy data")
        book = library_service.get_book_by_title('Banana book')
        lending_service.borrow_book(reader, book, datetime.datetime.strptime('2025-01-01', "%Y-%m-%d").date()) # not due

        book = library_service.get_book_by_title('Banana book2')
        lending_service.borrow_book(reader, book, datetime.datetime.strptime('2024-12-01', "%Y-%m-%d").date()) # overdue

        book = library_service.get_book_by_title('Banana book3')
        lending_service.borrow_book(reader, book, datetime.datetime.strptime('2025-01-01', "%Y-%m-%d").date()) # not due

      elif choice == '11': # Create reader card for reader
        reader_id = input("Enter reader ID: ").strip()

        if not reader_id or not reader_id.isalnum():
          menu_view.display_error_msg(f'Ivalid reader ID: \'{reader_id}\'. Please use numbers and letters only.')
          continue

        reader = reader_service.get_reader(reader_id)
        reader_card_id = reader.get_reader_card()
        if reader_card_id:
          menu_view.display_error_msg(f"Reader {reader.name} already have reader card '{reader_card_id}'")
          continue

        reader_card = reader_service.register_reader_card (reader)

        menu_view.display_success_msg(f"Reader card {reader_card.card_id} created for {reader_card.reader_id}")

      else:
        menu_view.display_error_msg("Invalid menu choice. Please try again.")

      # save to file on every menu finish
      reader_card_nums = reader_service.get_used_reader_card_numbers()
      file_save = save_to_pickle(const.LIBRARY_DATA_FILENAME, library_service.books, lending_service.borrowed_books, reader_service.readers, reader_card_nums, reader_service.reader_cards, auth_service.users)
      if const.ENVIRONMENT == 'dev':
        if file_save is True:
          system_view.display_system_msg(f"Data saved to {const.LIBRARY_DATA_FILENAME}")
        else:
          system_view.display_system_msg(f"Error: {file_save}")

    except Exception as e:
      print(f"An unexpected error occurred: {e}")
      if const.ENVIRONMENT == 'dev':
        print(traceback.format_exc())

if __name__ == "__main__":
  main()


