from flask import Blueprint, request, render_template, redirect, jsonify
from flask_security.decorators import auth_required, roles_accepted
from app.extentions.extentions import eleven_client, chain_reading


listening_view = Blueprint('listening_view', __name__)

@listening_view.route('/hoc-tieng-anh/listening')
@auth_required()
def get_listening_page():
    return render_template('listening.html')

    
@listening_view.route('/api/v1/listening/check', methods=['POST'])
def listening_check():
    form = request.form

    if 'audio-upload' not in request.files:
        return jsonify(message='Chưa upload file audio'), 404
    
    audio_file = request.files['audio-upload']
    transcript = eleven_client.speech_to_text.convert(file=audio_file, language_code='en', model_id='scribe_v1')
    
    questions = form.get('questions')
    respond = chain_reading.invoke(input={'Passage': transcript.text, 'Questions': questions})
    return jsonify(result=respond)
        


