from flask import Blueprint, request, render_template, jsonify
from flask_security.decorators import auth_required, roles_accepted
from app.extentions.extentions import eleven_client, chain_speaking
from flask_login import current_user


speaking_view = Blueprint('speaking_view', __name__)

@speaking_view.route('/hoc-tieng-anh/speaking')
@roles_accepted('USER')
@auth_required()
def speaking_page():
    return render_template('speaking.html')

@speaking_view.route('/hoc-tieng-anh/speaking/talk-with-ai')
@roles_accepted('USER')
@auth_required()
def speaking_with_ai_page():
    return render_template('speaking_ai.html')


@speaking_view.route('/api/v1/speaking/ai/upload', methods=['POST'])
@auth_required()
def speaking_ai():
    if 'file' not in request.files:
        return jsonify(message='Không có bản ghi record'), 400
    
    file = request.files['file']
    transcription = eleven_client.speech_to_text.convert(file=file, language_code='en', model_id='scribe_v1')


    response = chain_speaking.invoke({'sentence_speaking': transcription.text}, config={'configurable': {'session_id': current_user.fs_uniquifier}})
    return jsonify(result={'user': transcription.text, 'ai': response.content}), 200

    

