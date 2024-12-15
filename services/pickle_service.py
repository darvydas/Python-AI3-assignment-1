import os
import pickle
# TODO: should split to multiple files
# TODO: args should contain only the data to save
def save_to_pickle(filename, library_service, lending_service, reader_service, auth_service):
  """Saves the library data to a pickle file."""
  try:
    # Create the 'db' directory if it doesn't exist
    if not os.path.exists('db'):
      os.makedirs('db')

    data = {
      'books': library_service.books,
      'borrowed_books': lending_service.borrowed_books,
      'readers': reader_service.readers,
      '__reader_card_nums': reader_service.__reader_card_nums,
      'reader_cards':reader_service.reader_cards,
      'users':auth_service.users
    } #TODO: add login data

    with open(filename, 'wb') as file:
      pickle.dump(data, file)
    return True

  except (FileNotFoundError, pickle.PickleError, OSError) as e:
    return f"Error saving data: {e}"





def load_from_pickle(filename, library_service, lending_service, reader_service, auth_service):
  """Loads the library data from a pickle file if it exists."""
  if os.path.exists(filename):  # Check if the file exists
    try:
      with open(filename, 'rb') as file:
          data = pickle.load(file)
      library_service.books = data['books']
      lending_service.borrowed_books = data['borrowed_books']
      reader_service.readers = data['readers']
      reader_service.__reader_card_nums = data['__reader_card_nums']
      reader_service.reader_cards = data['reader_cards']

      #TODO: add login data
      return True
    except (EOFError, pickle.UnpicklingError) as ex:  # Handle potential errors during loading
      return f"Error loading data from file. {ex}"
  else:
    return f"No saved data found on {filename}."
