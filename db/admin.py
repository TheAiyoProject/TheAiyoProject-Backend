from sqladmin import ModelView
from db.models import User

class UserAdmin(ModelView, model=User):
   pass