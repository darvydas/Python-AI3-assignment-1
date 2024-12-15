def display_librarian_menu():
  """Displays the main menu options."""
  print("\nLibrary Management System")
  print("1. Add book")
  print("2. Remove book")
  print("3. Find book")
  print("4. Display all books")
  print("5. Create new reader with reader card")
  print("6. View overdue books")
  print("7. View borrowed books")
  print("8. Exit")
  print("9. Add dummy data")

def display_reader_menu():
  """Displays the main menu options."""
  print("\nLibrary Management System")
  print("1. Display all books")
  print("2. Find book")
  print("3. Borrow book")
  print("4. Return book")
  print("5. Show my borrowed books")
  print("6. Exit")

def display_login_menu():
  """Displays login menu options."""
  print("\nLibrary Management System")
  print("1. Librarian login")
  print("2. Reader card ID")
  print("3. Register new librarian")

def display_success_msg(msg):
  print(f"\nSuccess: {msg}")

def display_error_msg(msg):
  print(f"\nError: {msg}")

def display_info_msg(msg):
  print(f"\nInfo: {msg}")
