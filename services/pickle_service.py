import os
import pickle

def save_to_pickle(filename, library_service, lending_service):
  """Saves the library data to a pickle file."""
  try:
    # Create the 'db' directory if it doesn't exist
    if not os.path.exists('db'):
      os.makedirs('db')

    data = {
      'books': library_service.books,
      'borrowed_books': lending_service.borrowed_books,
      'readers': lending_service.readers,
    }

    with open(filename, 'wb') as file:
      pickle.dump(data, file)
    return True

  except (FileNotFoundError, pickle.PickleError, OSError) as e:
    return f"Error saving data: {e}"
  except Exception as e:
    return f"An unexpected error occurred: {e}"





def load_from_pickle(filename, library_service, lending_service):
  """Loads the library data from a pickle file if it exists."""
  if os.path.exists(filename):  # Check if the file exists
    try:
      with open(filename, 'rb') as file:
          data = pickle.load(file)
      library_service.books = data['books']
      lending_service.borrowed_books = data['borrowed_books']
      lending_service.readers = data['readers']

      return True
    except (EOFError, pickle.UnpicklingError) as ex:  # Handle potential errors during loading
      return f"Error loading data from file. {ex}"
    except Exception as e:
      return f"An unexpected error occurred: {e}"
  else:
    return f"No saved data found on {filename}."