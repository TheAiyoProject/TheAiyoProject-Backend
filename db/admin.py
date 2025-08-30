from sqladmin import ModelView
from db.models import User, Profile, VerificationOTP

class UserAdmin(ModelView, model=User):
   pass

class ProfileAdmin(ModelView, model=Profile):
   pass

class VerificationOTPAdmin(ModelView, model=VerificationOTP):
   pass