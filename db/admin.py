from sqladmin import ModelView
from db.models import User, Profile

class UserAdmin(ModelView, model=User):
   pass

class ProfileAdmin(ModelView, model=Profile):
   pass