from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, JSON, ForeignKey, create_engine,Text,Date, UniqueConstraint, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
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


class User(Base):
    __tablename__= 'users'

    id= Column(Integer, primary_key=True)
    email= Column(String(255), unique=True, nullable=False)
    password= Column(String(255), nullable=False)
    joined_at= Column(DateTime, default=datetime.now())
    is_verified= Column(Boolean, default=False)
    is_active= Column(Boolean, default=True)
    is_admin= Column(Boolean, default=False)

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
