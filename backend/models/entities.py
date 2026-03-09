from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    avatars = relationship("Avatar", back_populates="user")


class Avatar(Base):
    __tablename__ = "avatars"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_url = Column(String, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    gender = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="avatars")
    try_on_results = relationship("TryOnResult", back_populates="avatar")


class Clothes(Base):
    __tablename__ = "clothes"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    try_on_results = relationship("TryOnResult", back_populates="clothes")


class TryOnResult(Base):
    __tablename__ = "try_on_results"

    id = Column(Integer, primary_key=True, index=True)
    avatar_id = Column(Integer, ForeignKey("avatars.id"), nullable=False)
    clothes_id = Column(Integer, ForeignKey("clothes.id"), nullable=False)
    result_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    avatar = relationship("Avatar", back_populates="try_on_results")
    clothes = relationship("Clothes", back_populates="try_on_results")
