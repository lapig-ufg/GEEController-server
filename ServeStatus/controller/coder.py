from flask import Blueprint, current_app, request, jsonify
from ServeStatus.model import Coder






bp_coder = Blueprint('coder', __name__,url_prefix ='/coder')


@bp_coder.route('/get/<string:version>', methods=['GET'])
def get_coder(version):
    try:
        coder = Coder.objects(version = version).all().order_by('-date').first()
        return jsonify({
            'coder': coder.code,
            'version':version,
            'date':coder.date
        }),201
    except Exception as e:
        return jsonify([{
            'state':'error',
            'error': str(e) ,
            'messagem':'Erro a gerar a lista'}])

@bp_coder.route('/send', methods=['POST'])
def send_coder():
    try:
        record = request.json
        coder = Coder(**record)
        coder.save()
        return jsonify(coder.to_json()),201
    except Exception as e:
        return jsonify([{
            'state':'error',
            'error': str(e) ,
            'messagem':'Erro a gerar a lista'}])