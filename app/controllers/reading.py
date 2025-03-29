from flask import Blueprint, request, render_template, redirect, session, jsonify
from flask_security import auth_required, roles_required
from app.extentions.extentions import chain_reading

reading_view = Blueprint('reading_view', __name__)

@reading_view.route('/hoc-tieng-anh/reading')
@roles_required('USER')
@auth_required()
def get_reading_page():
    return render_template('reading.html')

    

@reading_view.route('/api/v1/reading/check', methods=['POST'])
def check():
    json_data = request.get_json()
    passage = json_data.get('passage')
    questions = json_data.get('questions')

    respond = chain_reading.invoke(input={'Passage': passage, 'Questions': questions})
    return jsonify(result=respond)


    