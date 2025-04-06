# from flask_admin import Admin, BaseView, expose
# from app.models.models import db, User, Role
# from flask_admin.contrib.sqla import ModelView
# from flask_admin import AdminIndexView
# from flask_login import current_user
# from flask import redirect, request
# # from flask_paginate import get_page_args, Pagination, get_page_parameter



# class SecureModelView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.is_authenticated and any(role.name == 'ADMIN' for role in current_user.roles)  # Bạn có thể kiểm tra quyền truy cập ở đây

#     def inaccessible_callback(self, name, **kwargs):
#         # redirect to login page if user doesn't have access
#         return redirect('/dang-nhap')

    
# class MyModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and any(role.name == 'ADMIN' for role in current_user.roles)  # Bạn có thể kiểm tra quyền truy cập ở đây
#         # return True
    
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect('/dang-nhap')

# class RoleView(MyModelView):
#     column_list = ['name', 'users']

# class UserView(MyModelView):
#     column_list = ['id', 'email', 'active', 'confirmed_at', 'roles']


# admin = Admin(name='EnglishS', template_mode='bootstrap4', index_view=SecureModelView())

# admin.add_view(UserView(User, db.session))
# admin.add_view(RoleView(Role, db.session))
