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


class Reading(db.Model):
    __tablename__ = 'reading'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column('title', String(500), nullable=False)
    content: Mapped[str] = mapped_column('content', Text, nullable=False)

    questions: Mapped[List['Question']] = relationship(back_populates='reading', cascade='all, delete-orphan', lazy=True)

    def __str__(self):
        return self.title
    
    def get_questions(self) -> 'Question':
        return self.questions

class QuestionType(db.Model):
    __tablename__ = 'question_type'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column('type', String(500), nullable=False, unique=True)

    def __str__(self):
        return self.type

class Question(db.Model):
    __tablename__ = 'question'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column('text', Text, nullable=False)
    
    question_type_id: Mapped[int] = mapped_column('question_type_id', ForeignKey('question_type.id'))
    question_type: Mapped['QuestionType'] = relationship(lazy=True)

    reading_id: Mapped[int] = mapped_column('reading_id', ForeignKey('reading.id'))
    reading: Mapped['Reading'] = relationship(back_populates='questions', lazy=True)

    answers: Mapped[List['Answer']] = relationship(back_populates='question', lazy=True, cascade='all, delete-orphan')

    def __str__(self):
        return f'reading:{self.reading.title}, question: {self.text}'
    
    def get_answers(self) -> 'Answer':
        return self.answers


class Answer(db.Model):
    __tablename__ = 'answer'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column('text', Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column('is_correct', nullable=False)

    question_id: Mapped[int] = mapped_column('question_id', ForeignKey('question.id'))
    question: Mapped['Question'] = relationship(back_populates='answers', lazy=True)

    def __str__(self):
        return self.text


class Listening(db.Model):
    __tablename__ = 'listening'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column('title', String(500), nullable=False)
    url: Mapped[str] = mapped_column('text', String(300), nullable=False)

    questions_listening: Mapped[List['QuestionListening']] = relationship(back_populates='listening', cascade='all, delete-orphan', lazy=True)

    def __str__(self):
        return self.title

class QuestionListening(db.Model):
    __tablename__ = 'question_listening'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column('text', Text, nullable=False)
    
    question_type_id: Mapped[int] = mapped_column('question_type_id', ForeignKey('question_type.id'))
    question_type: Mapped['QuestionType'] = relationship(lazy=True)

    listening_id: Mapped[int] = mapped_column('listening_id', ForeignKey('listening.id'))
    listening: Mapped['Listening'] = relationship(back_populates='questions_listening', lazy=True)

    answers: Mapped[List['AnswerListening']] = relationship(back_populates='question_listening', lazy=True, cascade='all, delete-orphan')

    def __str__(self):
        return f'listening:{self.listening.title}, question: {self.text}'

class AnswerListening(db.Model):
    __tablename__ = 'answer_listening'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column('text', Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column('is_correct', nullable=False)

    question_listening_id: Mapped[int] = mapped_column('question_listening_id', ForeignKey('question_listening.id'))
    question_listening: Mapped['QuestionListening'] = relationship(back_populates='answers', lazy=True)

    def __str__(self):
        return self.text



