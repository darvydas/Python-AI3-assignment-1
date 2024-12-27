import datetime

class ReaderCard:
  def __init__(self, card_id, reader_id, issue_date = datetime.date.today()):
    self.card_id = card_id
    self.reader_id = reader_id
    self.issue_date = issue_date

  def __str__(self):
    return f"Card ID: {self.card_id}, Reader ID: {self.reader_id}, Issued: {self.issue_date}"
