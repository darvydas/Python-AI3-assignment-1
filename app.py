# main.py

from models.book import Book
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
      print("Book added successfully!")

    elif choice == '2':
      title = input("Enter title of book to remove: ")
      removed_book = library_service.remove_book(title)
      if removed_book:
        print(f"Book \"{removed_book.title}\" by {removed_book.author} removed from library!")
      else:
        print("Book not found.")

    elif choice == '3':
      query = input("Enter title or author to search: ")
      results = library_service.find_book(query)
      library_view.display_search_results(results)

    elif choice == '4':
      library_view.display_all_books(library_service.books)

    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
  main()
