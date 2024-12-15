from datetime import date
import os
import pickle
# TODO: could split saving to multiple methods/files

def save_to_pickle(filename, books, borrowed_books, readers, reader_card_nums, reader_cards, users):
  """Saves the library data to a pickle file."""
  try:
    # Create the 'db' directory if it doesn't exist
    if not os.path.exists('db'):
      os.makedirs('db')

    data = {
      'books':          books,
      'borrowed_books': borrowed_books,
      'readers':        readers,
      'reader_card_nums': reader_card_nums,
      'reader_cards':   reader_cards,
      'users':          users
    }

    with open(filename, 'wb') as file:
      pickle.dump(data, file)
    return True

  except (FileNotFoundError, pickle.PickleError, OSError) as e:
    return f"Error saving data: {e}"

def load_from_pickle(filename):
  """Loads the library data from a pickle file if it exists."""
  if os.path.exists(filename):  # Check if the file exists
    try:
      with open(filename, 'rb') as file:
        data = pickle.load(file)
      file_data = {
      'books':          data['books'],
      'borrowed_books': data['borrowed_books'],
      'readers':        data['readers'],
      'reader_card_nums': data['reader_card_nums'],
      'reader_cards':   data['reader_cards'],
      'users':          data['users']
    }
      return True, file_data
    except (EOFError, pickle.UnpicklingError) as ex:  # Handle potential errors during loading
      return False, f"Error loading data from file. {ex}"
  else:
    return False, f"No saved data found on {filename}."
