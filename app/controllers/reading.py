from flask import Blueprint, request, render_template, redirect, session, jsonify
from flask_security import auth_required, roles_required
from app.models.models import Reading

reading_view = Blueprint('reading_view', __name__)

@reading_view.route('/hoc-tieng-anh/reading')
@roles_required('USER')
@auth_required()
def get_reading_page():
    readings = Reading.query.all()
    return render_template('reading.html', readings=readings)

@reading_view.route('/hoc-tieng-anh/reading/<int:reading_id>')
def get_reading_lessson(reading_id):
    reading = Reading.query.get(ident=reading_id)
    submit_result = session.get('submit_result', None)
    if not reading:
        return redirect('page_not_found')
    return render_template('reading_lesson.html', reading=reading, submit_result=submit_result)

# @reading_view.route('/hoc-tieng-anh/reading/<int:reading_id>', methods=['POST'])
# def submit_reading_answer(reading_id):

@reading_view.route('/api/v1/reading/answer-choose', methods=['POST'])
def choose_answer():
    json_data = request.get_json()
    question = json_data.get('question')

    answer = json_data.get('answer')

    session[question] = answer
    return jsonify(message='Success'), 200

@reading_view.route('/api/v1/reading/<int:reading_id>', methods=['POST'])
def submit_reading(reading_id):
    form = request.form
    submit_result = {}
    reading = Reading.query.get(ident=reading_id)
    questions = reading.questions
    for question in questions:
        print(question)
        i = 0
        answers = question.answers
        answer_pick = int(form.get(f'{question.id}'))
        while (i < len(answers)):
            if answer_pick == answers[i].id and answers[i].is_correct:
                submit_result[f'{question.id}'] = {'is_correct': True, 'answer_pick': answers[i].id}
                session.pop(str(question.id), None)

                break
            elif answer_pick == answers[i].id and answers[i].is_correct == False:
                submit_result[f'{question.id}'] = {'is_correct': False, 'answer_pick': answers[i].id}
                session.pop(str(question.id), None)

                break
            i+=1
            
    session['submit_result'] = submit_result
    print(submit_result)

    
    return redirect(f'/hoc-tieng-anh/reading/{reading_id}')
    # print(int(form.get('1')))
    # return 'Test'

@reading_view.route('/api/v1/reading/reset', methods=['POST'])
@auth_required()
def reset_reading():
    session.pop('submit_result', None)
    return jsonify(message='Success'), 200


    