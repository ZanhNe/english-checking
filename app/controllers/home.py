from flask import Blueprint, render_template, redirect
home_view = Blueprint('home_view', __name__)


@home_view.route('/', methods=['GET'])
def base():
    return redirect('trang-chu')

@home_view.route('/trang-chu', methods=['GET'])
def trang_chu():
    return render_template('home.html')

@home_view.route('/test', methods=['GET'])
def test():
    return render_template('test.html')