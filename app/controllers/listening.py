from flask import Blueprint, request, render_template, redirect, session
from flask_login import current_user
from flask_security.decorators import auth_required, roles_accepted
from app.extentions.extentions import eleven_client
from app.models.models import Listening, db
import cloudinary.uploader
import io
import os

listening_view = Blueprint('listening_view', __name__)

@listening_view.route('/hoc-tieng-anh/listening')
def get_listening_page():
    listenings = Listening.query.all()
    return render_template('listening.html', listenings=listenings)

@listening_view.route('/hoc-tieng-anh/listening/<int:listening_id>', methods=['GET'])
@auth_required()
def get_listening_lesson(listening_id):
    listening = Listening.query.get(ident=listening_id)
    print(listening)
    submit_result = session.get('submit_result', None)
    if not listening:
        return redirect('page_not_found'), 404
    return render_template('listening_lesson.html', listening=listening, submit_result=submit_result)


@listening_view.route('/api/v1/listening/<int:listening_id>', methods=['POST'])
def submit_listening(listening_id):
    pass

@listening_view.route('/admin/listening/create', methods=['POST'])
# @roles_accepted('ADMIN')
# @auth_required()
def create_listening_lesson():
    try:
        form = request.form
        title = form.get('title')
        transcript = form.get('transcript')
        audio_generator = eleven_client.text_to_speech.convert(
                    voice_id="EXAVITQu4vr4xnSDxMaL",
                    output_format="mp3_44100_128",
                    text=transcript,
                    model_id="eleven_multilingual_v2",
                    enable_logging=True
            )
        audio_bytes = b''.join(audio_generator)
        audio_file = io.BytesIO(initial_bytes=audio_bytes)


        response = cloudinary.uploader.upload(file=audio_file,
                                                resource_type="video",
                                                folder="audio_files",
                                                public_id="my_audio_file",
                                                format="mp3")

        listening = Listening(title=title, url=response['secure_url'])

        db.session.add(instance=listening)
        db.session.commit()
        return redirect('/admin/listening/create')
    except Exception as e:
        db.session.rollback()
        return redirect('/admin/listening')
    
    

        


