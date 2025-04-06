from flask import Blueprint, request, render_template, redirect, jsonify
from flask_security.decorators import auth_required, roles_accepted
from app.extentions.extentions import eleven_client, chain_reading
from docx import Document
from pypdf import PdfReader


listening_view = Blueprint('listening_view', __name__)

@listening_view.route('/hoc-tieng-anh/listening')
def get_listening_page():
    return render_template('listening.html')

@listening_view.route('/hoc-tieng-anh/listening-uploads')
def get_listening_upload_page():
    return render_template('listening_upload.html')


    
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
        

@listening_view.route('/api/v1/listening/uploads', methods=['POST'])
def listening_upload_check():
    if 'audio-upload' not in request.files:
        return jsonify(message='Chưa upload file audio'), 400
    if 'file' not in request.files:
        return jsonify(message='Chưa upload file câu hỏi'), 400
    audio_file = request.files['audio-upload']
    transcript = eleven_client.speech_to_text.convert(file=audio_file, language_code='en', model_id='scribe_v1')
    file = request.files['file']
    if file.filename.endswith('.docx'):
        document = Document(file)
        text = "\n".join([para.text.lower() for para in document.paragraphs if para.text.lower() != 'question'])
        
        respond = chain_reading.invoke(input={'Passage': transcript.text, 'Questions': text})
        return jsonify(results=respond)
    if file.filename.endswith('.pdf'):
        reader = PdfReader(file)
        text = "".join([page.extract_text().lower() for page in reader.pages if page.extract_text().lower() != 'question'])
        respond = chain_reading.invoke(input={'Passage': transcript.text, 'Questions': text})
        return jsonify(results=respond)
    return jsonify(message='Không hỗ trợ định dạng này, vui lòng thử lại định dạng hệ thống hỗ trợ: docx, pdf'), 400

