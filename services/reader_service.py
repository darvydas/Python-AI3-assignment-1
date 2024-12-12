from models.reader import Reader
from models.readerCard import ReaderCard

class ReaderService:
  def __init__(self):
    self.readers = {}  # Dictionary to store readers by their ID

  def get_or_create_reader(self, reader_id, reader_name="Unknown"):
    """
    Gets an existing reader or creates a new one if not found.
    Returns: A Reader object.
    """
    if reader_id not in self.readers:
      self.readers[reader_id] = Reader(reader_name, reader_id)
    return self.readers[reader_id]

  def get_reader(self, reader_id):
    """
    Gets the Reader object with the given reader_id.
    Returns: Reader object if found, None otherwise.
    """
    return self.readers.get(reader_id)
