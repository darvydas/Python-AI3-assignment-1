import os
import pickle

def save_to_pickle(filename, library_service, lending_service):
  """Saves the library data to a pickle file."""

  # Create the 'db' directory if it doesn't exist
  if not os.path.exists('db'):
    os.makedirs('db')

  data = {
    'books': library_service.books,
    'borrowed_books': lending_service.borrowed_books
  }

  with open(filename, 'wb') as file:
      pickle.dump(data, file)
  print(f"Data saved to {filename}")

def load_from_pickle(filename, library_service, lending_service):
  """Loads the library data from a pickle file if it exists."""
  if os.path.exists(filename):  # Check if the file exists
      try:
          with open(filename, 'rb') as file:
              data = pickle.load(file)
          library_service.books = data['books']
          lending_service.borrowed_books = data['borrowed_books']
          # ... load other data ...
          print(f"Data loaded from {filename}")
      except (EOFError, pickle.UnpicklingError):  # Handle potential errors during loading
          print("Error loading data from file.")
  else:
      print(f"No saved data found on {filename}.")