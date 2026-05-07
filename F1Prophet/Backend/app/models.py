from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    total_points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    predictions = relationship('Prediction', back_populates='user', cascade='all, delete-orphan')

class Race(Base):
    __tablename__ = 'races'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    race_date = Column(DateTime, nullable=False)
    deadline = Column(DateTime, nullable=False)
    season = Column(Integer, nullable=False)
    round_number = Column(Integer, nullable=False)
    status = Column(Enum('upcoming', 'active', 'completed'), default='upcoming')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    predictions = relationship('Prediction', back_populates='race', cascade='all, delete-orphan')
    results = relationship('RaceResult', back_populates='race', cascade='all, delete-orphan')

class Prediction(Base):
    __tablename__ = 'predictions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    race_id = Column(Integer, ForeignKey('races.id'), nullable=False)
    fastest_lap = Column(String(50))
    submitted_at = Column(DateTime, default=datetime.utcnow)
    points_earned = Column(Integer)
    
    user = relationship('User', back_populates='predictions')
    race = relationship('Race', back_populates='predictions')
    positions = relationship('PredictedPosition', back_populates='prediction', cascade='all, delete-orphan')

class PredictedPosition(Base):
    __tablename__ = 'predicted_positions'
    
    id = Column(Integer, primary_key=True)
    prediction_id = Column(Integer, ForeignKey('predictions.id'), nullable=False)
    driver_id = Column(String(50), nullable=False)
    position = Column(Integer)
    is_dnf = Column(Boolean, default=False)
    
    prediction = relationship('Prediction', back_populates='positions')

class RaceResult(Base):
    __tablename__ = 'race_results'
    
    id = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey('races.id'), nullable=False)
    driver_id = Column(String(50), nullable=False)
    position = Column(Integer)
    is_dnf = Column(Boolean, default=False)
    fastest_lap = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    race = relationship('Race', back_populates='results')