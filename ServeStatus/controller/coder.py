from flask import Blueprint, request, jsonify
from ServeStatus.model import Coder
from flask_cors import cross_origin
from ServeStatus.functions import is_lapig_user




bp_coder = Blueprint('coder', __name__,url_prefix ='/coder')


@bp_coder.route('/get/<string:version>', methods=['GET'])
@cross_origin()
@is_lapig_user
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
@cross_origin()
@is_lapig_user
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