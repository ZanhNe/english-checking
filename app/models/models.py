from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Column, ForeignKey, Boolean, DateTime, Text, Enum
from flask_security import UserMixin, RoleMixin
# from flask_login import UserMixin
from typing import List, Optional
import enum
import uuid

class Base(DeclarativeBase):

    pass

db = SQLAlchemy(model_class=Base)

roles_users = db.Table('roles_users', 
                    Column('user_id', ForeignKey('user.id'), primary_key=True), 
                    Column('role_id', ForeignKey('role.id'), primary_key=True))





class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column('name', String(10), nullable=False, unique=True)

    users: Mapped[List['User']] = relationship(back_populates='roles', secondary=roles_users, lazy=True)

    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column('email', String(300), nullable=False, unique=True)
    password: Mapped[str] = mapped_column('password', String(200), nullable=False)
    display_name: Mapped[str] = mapped_column('display_name', String(400), nullable=True)
    fs_uniquifier: Mapped[str] = mapped_column('fs_uniquifier', String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4)) # Trường bắt buộc từ Flask-Security-Too 4.0.0+
    active: Mapped[bool] = mapped_column('active', Boolean)
    confirmed_at: Mapped[Optional[DateTime]] = mapped_column('confirmed_at', DateTime, nullable=True)
    roles: Mapped[List['Role']] = relationship(back_populates='users', secondary=roles_users, lazy=True)

    def __str__(self):
        return f'user_{self.id}:{self.email}'





