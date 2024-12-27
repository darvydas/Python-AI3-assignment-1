from datetime import date, datetime
import os
import pickle
import mysql.connector
import sqlite3
from constants import LIBRARY_DATA_FILENAME, PERSISTENCE_METHOD, SQLITE_FILENAME, MYSQL_CONFIG

from models.book import Book
from models.readerCard import ReaderCard
from models.reader import Reader
from models.user import User
from models.role import Role

# TODO: could split saving to multiple methods/files

def initiate_mysql():
  conn = mysql.connector.connect(
    host=MYSQL_CONFIG['host'],
    user=MYSQL_CONFIG['user'],
    password=MYSQL_CONFIG['password'],
    database=MYSQL_CONFIG['database']
  )
  # cursor = conn.cursor()
  # #create table if not exists books (title, author, publication_year, genre, available)
  # cursor.execute("""
  #   CREATE TABLE IF NOT EXISTS books (
  #     title VARCHAR(255) PRIMARY KEY NOT NULL,
  #     author VARCHAR(255),
  #     publication_year DATE,
  #     genre VARCHAR(255),
  #     available INT
  #   )""")
  # conn.commit()
  return conn

def initialize_sqlite():
  conn = sqlite3.connect(SQLITE_FILENAME)
  c = conn.cursor()
  #create sqlite3 table if not exists books (title, author, publication_year, genre, available)

  c.execute("""
    CREATE TABLE IF NOT EXISTS books (
      title text PRIMARY KEY UNIQUE NOT NULL,
      author text,
      publication_year text,
      genre text,
      available integer
    )""")
  conn.commit()

  c.execute("""
    CREATE TABLE IF NOT EXISTS reader_cards (
      id text PRIMARY KEY NOT NULL UNIQUE,
      reader_id text,
      issue_date text,
      card_id text
    )""")
  conn.commit()

  c.execute("""
    CREATE TABLE IF NOT EXISTS readers (
      id text PRIMARY KEY NOT NULL UNIQUE,
      name text,
      card_id text,
      FOREIGN KEY (card_id) REFERENCES reader_cards(id)
    )""")
  conn.commit()

  c.execute("""
    CREATE TABLE IF NOT EXISTS borrowed_books (
      book_title text NOT NULL,
      due_date text,
      reader_id text NOT NULL,
      PRIMARY KEY (book_title, reader_id),
      FOREIGN KEY (book_title) REFERENCES books(title),
      FOREIGN KEY (reader_id) REFERENCES readers(id)
    )""")
  conn.commit()

  c.execute("""
    CREATE TABLE IF NOT EXISTS users (
      username text PRIMARY KEY NOT NULL UNIQUE,
      password text,
      role text,
      card_id text
    )""")
  conn.commit()

  conn.close()
  return conn

def save_to_sqlite(books, borrowed_books, readers, reader_card_nums, reader_cards, users):
  conn = sqlite3.connect(SQLITE_FILENAME)
  # save books to sqlite books table
  cursor = conn.cursor()
  for book in books: # [Book(title, author, publication_year, genre, _available)]
    cursor.execute("INSERT OR REPLACE INTO books (title, author, publication_year, genre, available) VALUES (?, ?, ?, ?, ?)", (book.title, book.author, book.publication_year, book.genre, book._available))
  conn.commit()

  # save borrowed_books to sqlite borrowed_books table
  for book, borrow_info_list in borrowed_books.items():
    for borrow_info in borrow_info_list:
      cursor.execute("INSERT OR REPLACE INTO borrowed_books (book_title, due_date, reader_id) VALUES (?, ?, ?)",
                     (book.title, datetime.strftime(borrow_info['due_date'], "%Y-%m-%d"), borrow_info['card_id']))
  conn.commit()

  # save readers to sqlite readers table
  for reader_id, reader in readers.items():
    cursor.execute("INSERT OR REPLACE INTO readers (id, name, card_id) VALUES (?, ?, ?)", (reader.id, reader.name, reader.get_reader_card_id()))
  conn.commit()

  # save reader_cards to sqlite reader_cards table
  for card_id, reader_card in reader_cards.items():
    cursor.execute("INSERT OR REPLACE INTO reader_cards (id, reader_id, issue_date, card_id) VALUES (?, ?, ?, ?)",
                   (reader_card.card_id.split('_')[1], # save reader_card_num
                    reader_card.reader_id, reader_card.issue_date, reader_card.card_id))
  conn.commit()

  # save into users
  for username, user in users.items():
    cursor.execute("INSERT OR REPLACE INTO users (username, password, role, card_id) VALUES (?, ?, ?, ?)", (user.username, user.password, user.role.value, user.card_id))
  conn.commit()

  conn.close()
  return True


def load_from_sqlite():
  if os.path.exists(SQLITE_FILENAME):  # Check if the file exists
    try:
      conn = sqlite3.connect(SQLITE_FILENAME)
      with conn:
        cursor = conn.cursor()

      # select all books
        cursor.execute("SELECT title, author, publication_year, genre, available FROM books")
        books_data = cursor.fetchall()
        books = [Book(title, author, publication_year, genre, available) for title, author, publication_year, genre, available in books_data]

      # select all borrowed_books
        cursor.execute("SELECT book_title, due_date, reader_id FROM borrowed_books")
        borrowed_books_data = cursor.fetchall()

        borrowed_books = {}
        for book_title, due_date, reader_id in borrowed_books_data:
        # get Book by title
          book = next((book for book in books if book.title == book_title), None)
          if book:
            if book not in borrowed_books:
              borrowed_books[book] = []
            borrowed_books[book].append({'due_date': datetime.strptime(due_date, "%Y-%m-%d").date(), 'card_id': reader_id})
          else:
            pass
            # TODO: return error if failed to find borrowed book in book list

      # select reader cards
        cursor.execute("SELECT id, reader_id, issue_date, card_id FROM reader_cards")
        reader_cards_data = cursor.fetchall()
        reader_cards = {}
        reader_card_nums = []
        for id, reader_id, issue_date, card_id in reader_cards_data:
          reader_cards[card_id] = ReaderCard(card_id, reader_id, issue_date)
          # reader_card_nums are id's from reader_cards
          reader_card_nums.append(id)


      # select readers
        cursor.execute("SELECT id, name, card_id FROM readers")
        readers_data = cursor.fetchall()
        readers = {}
        for id, name, card_id in readers_data:
          reader = Reader(name, id)
          reader.set_reader_card(card_id)

          # find reader borrowed books from borrowed_books
          for book, borrow_info_list in borrowed_books.items():
            for borrow_info in borrow_info_list:
              if borrow_info['card_id'] == card_id:
                reader.borrowed_books.append(book)

          readers[id] = reader

        # get from users
        cursor.execute("SELECT username, password, role, card_id FROM users")
        users_data = cursor.fetchall()
        users = {}
        for username, password, role, card_id in users_data:
          users[username] = User(Role(role), username, password, card_id)



      db_data = {
      'books':            books,
      'borrowed_books':   borrowed_books,
      'readers':          readers,
      'reader_card_nums': reader_card_nums,
      'reader_cards':     reader_cards,
      'users':            users
    }
      return True, db_data
    except (EOFError, pickle.UnpicklingError) as ex:  # Handle potential errors during loading
      return False, f"Error loading data from file. {ex}"
  else:
    return False, f"No SQLite data found on {SQLITE_FILENAME}."

def save_data(books, borrowed_books, readers, reader_card_nums, reader_cards, users):
  """Saves data based on the chosen persistence method."""
  if PERSISTENCE_METHOD == "pickle":
    return save_to_pickle(LIBRARY_DATA_FILENAME, books, borrowed_books, readers, reader_card_nums, reader_cards, users)
  elif PERSISTENCE_METHOD == "sqlite":
    conn = initialize_sqlite()
    return save_to_sqlite(books, borrowed_books, readers, reader_card_nums, reader_cards, users)
  elif PERSISTENCE_METHOD == "mysql":
    # TODO: add error handling
    conn = initiate_mysql()
    return save_to_mysql(conn, books, borrowed_books, readers, reader_card_nums, reader_cards, users)
  else:
    return False, "Unsupported persistence method"

def load_data():
  """Loads data based on the chosen persistence method."""
  if PERSISTENCE_METHOD == "pickle":
    return load_from_pickle(LIBRARY_DATA_FILENAME)
  elif PERSISTENCE_METHOD == "sqlite":
    return load_from_sqlite()
  elif PERSISTENCE_METHOD == "mysql":
    return load_from_mysql(...)
  else:
    return False, "Unsupported persistence method"

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

def save_to_mysql(conn, books, borrowed_books, readers, reader_card_nums, reader_cards, users):
  """Saves the library data to a MySQL database."""
  try:
    cursor = conn.cursor()

    # Example: Save books data (adapt for your table structure)
    for book in books:
      cursor.execute("INSERT INTO books (title, author, publication_year, genre, available) VALUES (%s, %s, %s, %s, %s)", (book.title, book.author, book.publication_year, book.genre, book.available))

    conn.commit()
    return True

  except mysql.connector.Error as err:
    return f"Error saving data to MySQL: {err}"

  finally:
    if conn.is_connected():
      conn.close()

def load_from_mysql(MYSQL_CONFIG):
  """Loads the library data from a MySQL database."""
  try:

    # Example: Load books data (adapt for your table structure)
    cursor.execute("SELECT title, author, publication_year, genre, available FROM books")
    books = []
    for row in cursor:
      book = Book(row[0], row[1], row[2], row[3], row[4])
      books.append(book)

    # Load other data from the database similarly

    return True, {'books': books} # Add other data to the dictionary

  except mysql.connector.Error as err:
    return False, f"Error loading data from MySQL: {err}"

  finally:
    if mydb.is_connected():
      mydb.close()
