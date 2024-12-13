from models.role import Role
class User:
  def __init__(self, role, username, password_hash = "", card_id = "") -> None:
    self.role:Role = role
    self.username = username
    self.password = password_hash
    self.card_id = card_id

  def __str__(self) -> str:
    return f"Logged in user: {self.role}\nUsername: {self.username}{'\nCard ID: '+self.card_id if self.card_id else ''}"
