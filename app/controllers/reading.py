from flask import Blueprint, request, render_template, redirect, session, jsonify
from flask_security import auth_required, roles_required
from app.extentions.extentions import chain_reading
from docx import Document
from pypdf import PdfReader

reading_view = Blueprint('reading_view', __name__)

@reading_view.route('/hoc-tieng-anh/reading')
def get_reading_page():
    return render_template('reading.html')

@reading_view.route('/hoc-tieng-anh/reading-uploads')
def get_reading_upload_page():
    return render_template('reading_upload.html')

@reading_view.route('/api/v1/reading/check', methods=['POST'])
def check():
    json_data = request.get_json()
    passage = json_data.get('passage')
    questions = json_data.get('questions')

    respond = chain_reading.invoke(input={'Passage': passage, 'Questions': questions})
    print(respond)
    return jsonify(result=respond)

@reading_view.route('/api/v1/reading/uploads', methods=['POST'])
def check_reading_upload():
    if 'file' not in request.files:
        return jsonify(message='Chưa upload file'), 400
    file = request.files['file']
    if file.filename.endswith('.docx'):
        document = Document(file)
        text = "\n".join([para.text.lower() for para in document.paragraphs if para.text.lower() != 'passage'])
        results = text.split('question')
        if len(results) < 2:
            return jsonify(message='Vui lòng định dạng lại format file với Passage và Question tách rời'), 400
        passage, questions = results
        respond = chain_reading.invoke(input={'Passage': passage, 'Questions': questions})
        return jsonify(results=respond)
    if file.filename.endswith('.pdf'):
        reader = PdfReader(file)
        text = "".join([page.extract_text().lower() for page in reader.pages if page.extract_text().lower() != 'passage'])
        results = text.split('question')
        passage, questions = results
        respond = chain_reading.invoke(input={'Passage': passage, 'Questions': questions})
        return jsonify(results=respond)
    return jsonify(message='Không hỗ trợ định dạng này, vui lòng thử lại định dạng hệ thống hỗ trợ: docx, pdf'), 400

        


    