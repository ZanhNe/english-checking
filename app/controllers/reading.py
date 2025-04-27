from flask import Blueprint, request, render_template, jsonify
from app.AI.prompt_template import template_fix_reading_image
from app.AI.entry import chain_reading, client_gemini
from app.AI.base_structure import config_reading_gemini
from app.AI.base_structure import Reading
from docx import Document
from pypdf import PdfReader
from PIL import Image

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

    uploaded_files = request.files.getlist("file")
    if len(uploaded_files) == 1:
        file = uploaded_files[0]
        if file.filename.endswith('.docx'):
            document = Document(file)
            text = "\n".join([para.text.lower() for para in document.paragraphs if para.text.lower() != 'passage'])
            results = text.split('question')
            if len(results) < 2:
                return jsonify(message='Vui lòng định dạng lại format file với Passage và Question tách rời'), 400
            passage, questions = results
            respond = chain_reading.invoke(input={'Passage': passage, 'Questions': questions})
            return jsonify(results=respond)
        elif file.filename.endswith('.pdf'):
            reader = PdfReader(file)
            text = "".join([page.extract_text().lower() for page in reader.pages if page.extract_text().lower() != 'passage'])
            results = text.split('question')
            passage, questions = results
            respond = chain_reading.invoke(input={'Passage': passage, 'Questions': questions})
            return jsonify(results=respond)

        elif file.filename.endswith(('.jpeg', '.png', '.jpg')):
            image = Image.open(file.stream)
            respond = client_gemini.models.generate_content(config=config_reading_gemini, model='gemini-2.0-flash-exp', contents=[template_fix_reading_image, image])
            my_recipes: list[Reading] = respond.parsed

            results = [reading.model_dump() for reading in my_recipes]

            return jsonify(results=results)
    
    else:
        if any(file.filename.endswith(('.docx', '.pdf')) for file in uploaded_files):
            return jsonify(message='Vui lòng chỉ được phép upload nhiều ảnh, còn word hoặc pdf chỉ duy nhất 1'), 400
        list_files = []
        for file in uploaded_files:
            image = Image.open(file.stream)
            list_files.append(image)
        respond = client_gemini.models.generate_content(config=config_reading_gemini, model='gemini-2.0-flash-exp', contents=[template_fix_reading_image, *list_files])
        my_recipes: list[Reading] = respond.parsed

        results = [reading.model_dump() for reading in my_recipes]

        return jsonify(results=results)

    return jsonify(message='Không hỗ trợ định dạng này, vui lòng thử lại định dạng hệ thống hỗ trợ: docx, pdf'), 400

        


    