from models.reader import Reader
from models.readerCard import ReaderCard
import random

class ReaderService:
  def __init__(self, readers = {}, reader_card_nums = [], reader_cards = {}):
    self.readers = readers  # Dictionary to store readers by their ID
    self.__reader_card_nums = reader_card_nums  # unique card numbers
    self.reader_cards = reader_cards

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

  def __generate_unique_card_number(self):
    random_number = random.randint(1, 99999)
    while True:
      if random_number not in self.__reader_card_nums:
        self.__reader_card_nums.append(random_number)
        return str(random_number)

  def register_reader_card(self, reader:Reader):
    new_card_id = str(reader.id) + self.__generate_unique_card_number()

    reader_card = ReaderCard(new_card_id, reader.id)
    reader.set_reader_card(new_card_id)
    # save all reader cards
    self.reader_cards[new_card_id] = reader_card
    return reader_card

  def get_used_reader_card_numbers(self):
    return self.__reader_card_nums
