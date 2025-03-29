from flask import Blueprint, request, render_template, Response
from flask_security.decorators import auth_required, roles_required, roles_accepted
from app.extentions.extentions import chain_grammar, chain_grammar_general
import json
writing_view = Blueprint('writing_view', __name__)



@writing_view.route('/hoc-tieng-anh/writing', methods=['GET'])
@roles_accepted('USER')
@auth_required()
def get_writing_page():
    return render_template('writing.html')


@writing_view.route('/api/v1/agent/writing', methods=['POST'])
def agent_writing():
    json_data = request.get_json()
    text = json_data.get('text')
    response = chain_grammar.invoke({"sentence": text})
    json_str = json.dumps(response, ensure_ascii=False)
    return Response(json_str, mimetype='application/json')

@writing_view.route('/api/v1/writing/general-check', methods=['POST'])
def check_general_writing():
    json_data = request.get_json()
    text = json_data.get('text')
    response = chain_grammar_general.invoke({"sentence": text})
    json_str = json.dumps(response, ensure_ascii=False)
    return Response(json_str, mimetype='application/json')


