from flask_admin import Admin, BaseView, expose
from app.models.models import db, User, Role, Reading, QuestionType, Question, Answer, Listening as ListeningModel, QuestionListening, AnswerListening
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, request
from flask_paginate import get_page_args, Pagination, get_page_parameter



class SecureModelView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and any(role.name == 'ADMIN' for role in current_user.roles)  # Bạn có thể kiểm tra quyền truy cập ở đây

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/dang-nhap')

    
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and any(role.name == 'ADMIN' for role in current_user.roles)  # Bạn có thể kiểm tra quyền truy cập ở đây
        # return True
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/dang-nhap')

class RoleView(MyModelView):
    column_list = ['name', 'users']

class UserView(MyModelView):
    column_list = ['id', 'email', 'active', 'confirmed_at', 'roles']
    

class ReadingView(MyModelView):
    column_list = ['id', 'title', 'content', 'questions']

class QuestionTypeView(MyModelView):
    column_list = ['id', 'type']

class QuestionView(MyModelView):
    column_list = ['id', 'text', 'question_type', 'reading', 'answers']

class AnswerView(MyModelView):
    column_list = ['id', 'text', 'is_correct', 'question']

class Listening(BaseView):
    @expose('/')
    def index(self):
        
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        
        listenings_all = ListeningModel.query.all()
        listenings = ListeningModel.query.offset(offset=offset).limit(per_page).all()
        questions = QuestionListening.query.all()
        questions_type = QuestionType.query.all()

        listenings_count = len(listenings_all)
        questions_count = len(questions)
        questions_type_count = len(questions_type)

        pagination = Pagination(page=page, total=listenings_count, per_page=per_page, css_framework='bootstrap4')

        lastest_listening = listenings_all[-1] if listenings_count > 0 else None



        return self.render('admin/admin_listening.html'\
                           , listenings_count=listenings_count, questions_count=questions_count, listenings=listenings\
                            , questions_type_count=questions_type_count, lastest_listening=lastest_listening, pagination=pagination)
    
    @expose('/create')
    def create_page(self):
        return self.render('admin/admin_listening_create.html')
    

class QuestionListeningView(MyModelView):
    column_list = ['id', 'text', 'question_type', 'listening', 'answers']

class AnswerListeningView(MyModelView):
    column_list = ['id', 'text', 'is_correct', 'question_listening']

admin = Admin(name='EnglishS', template_mode='bootstrap4', index_view=SecureModelView())

admin.add_view(UserView(User, db.session))
admin.add_view(RoleView(Role, db.session))
admin.add_view(ReadingView(Reading, db.session, category='Reading'))
admin.add_view(QuestionTypeView(QuestionType, db.session, category='Reading'))
admin.add_view(QuestionView(Question, db.session, category='Reading'))
admin.add_view(AnswerView(Answer, db.session, category='Reading'))
admin.add_view(Listening(name='Listening', category='Listening'))

admin.add_view(QuestionListeningView(QuestionListening, db.session, category='Listening'))
admin.add_view(AnswerListeningView(AnswerListening, db.session, category='Listening'))