from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, JSON, ForeignKey, create_engine,Text,Date, UniqueConstraint, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
import random
load_dotenv()

DATABASE_URL= os.environ['DATABASE_URL']

engine= create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_platform_id():
    """Return random 8–10 digit string"""
    return str(random.randint(10**7, 10**10 - 1))

"""

def populate_platform_ids():
    with SessionLocal() as db:  # context manager automatically closes session
        users_without_pid = db.query(User).filter(User.platform_id == None).all()
        print(f"Found {len(users_without_pid)} users without platform_id")

        for user in users_without_pid:
            new_id = generate_platform_id()
            # optional uniqueness check:
            while db.query(User).filter(User.platform_id == new_id).first():
                new_id = generate_platform_id()
            user.platform_id = new_id

        db.commit()
        print("Platform IDs assigned successfully!")
"""
class User(Base):
    __tablename__= 'users'

    id= Column(Integer, primary_key=True)
    email= Column(String(255), unique=True, nullable=False)
    password= Column(String(255), nullable=False)
    joined_at= Column(DateTime, default=datetime.now())
    is_verified= Column(Boolean, default=False)
    is_active= Column(Boolean, default=True)
    is_admin= Column(Boolean, default=False)
    platform_id = Column(String(10), unique=True, nullable=False, default=generate_platform_id)  # 👈

    # Relationship with Profile
    profile= relationship("Profile", uselist=False, back_populates="user", cascade="all, delete-orphan")

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, password):
        self.password= pwd_context.hash(password)


    
    def __repr__(self):
        return self.email


class Profile(Base):
    __tablename__= 'profiles'

    id= Column(Integer, primary_key=True)
    user_id= Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)
    nickname= Column(String(255), nullable=True)
    personalization_questions= Column(JSON, nullable=True)


    user= relationship("User", back_populates="profile")

    def __repr__(self):
        return self.nickname or f"Profile {self.id}"
    
class VerificationOTP(Base):
    __tablename__ = 'verification_otps'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    otp = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    
    def is_valid(self):
        """Check if the OTP is still valid (not expired and not used)"""
        return datetime.now() < self.expires_at and not self.is_used
    
    def mark_as_used(self):
        """Mark this OTP as used"""
        self.is_used = True
