from models.user import User
from models.role import Role
import constants as const
import hashlib

class AuthenticationService:
  def __init__(self, users = {}) -> None:
    self.users:dict[User] = users #{'username':{username:str, password: str, card_id: str, role: Role}}
    self.logged_in = {}

  def generate_password_hash(self, pass_input:str) -> str:
    return hashlib.sha256(pass_input.encode()).hexdigest()

  def check_password(self, stored_hash, pass_input:str) -> bool:
    hashed_password = self.generate_password_hash(pass_input)
    return hashed_password == stored_hash

  def authenticate_librarian(self, username_input, password_input):
    user:User = self.users.get(username_input)
    if user and user.role == Role.LIBRARIAN and self.check_password(user.password, password_input):
      self.logged_in = user
      return user
    return False

  def register_librarian(self, username_input, password_input):
    password_hash = self.generate_password_hash(password_input)
    user = User(Role.LIBRARIAN, username_input, password_hash)
    self.users[username_input] = user # TODO: should save to file
    return user

  def validate_reader_card(self, card_id):
    if card_id: # TODO: unfinished validation
        return User(Role.READER, "", card_id=card_id)
    return False


