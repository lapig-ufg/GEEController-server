from flask import Blueprint, current_app, request, jsonify
from ServeStatus.app.model import Task
from Lapig.Functions import type_process, login_gee, error_in_task, id_
from dynaconf import settings
from sys import exit, version
import urllib3
import re


bp_task = Blueprint('task', __name__,url_prefix='/task')


@bp_task.route('/get/<string:version>/<string:run_class>', methods=['GET'])
def get_tasks(version,run_class):
    if run_class == 'all':
        task = Task.objects(state='IN_QUEUE',version=version).all()
    else:
        rgx = re.compile('.*{run_class}', re.IGNORECASE) 
        task = Task.objects(state='IN_QUEUE',version=version,name__contains=run_class).all()
    if not task:
        return jsonify([])
    else:
        return task.to_json(),200, {'ContentType':'application/json'} 

@bp_task.route('/runnig/<string:version>/<string:client>', methods=['GET'])
def get_runnig(version,client):
    task = Task.objects(
        version = version,
        state='RUNNING',
        client=client).all()
    if not task:
        return jsonify({})
    else:
        runnig = {i.id_:i.task_id for i in task}
        return runnig,200, {'ContentType':'application/json'} 

@bp_task.route('/completed/<string:version>', methods=['GET'])
def get_completed(version):#completed
    all_tasks = len(Task.objects(
        version = version).all())
    task = Task.objects(
        version = version,
        state='COMPLETED').all()
    error = Task.objects(
        version = version,
        state='ERROR').all()
    len_error = len(error)
    if not error:
        len_error = 0
        error = {}
    else:
        error = {i.id_:i.task_id for i in error}
    if not task:
        return jsonify([{'completed':0,
        'errors':0,
        'len':0, 'falta':all_tasks},{'task_ok':{},'task_error':{}}])
    else:
        completed = {i.id_:i.task_id for i in task}
        tamanho=len(completed)
        return jsonify([{
            'completed':tamanho,
            'errors': len_error,
            'falta':(all_tasks - (tamanho+len_error))
            },{
                'task_ok':completed,
                'task_error': error
        }]) ,200, {'ContentType':'application/json'} 


@bp_task.route('/errors/<string:version>', methods=['GET'])
def get_errors(version):#errors
    task = Task.objects(
        version = version,
        state='ERROR').all()
    if not task:
        return jsonify([{'len':0},{'task':{}}])
        
    else:
        errors = {i.id_:i.task_id for i in task}
        tamanho=len(errors)
        return jsonify([{'len':tamanho,'falta':(len(settings.LIST_OF_TASKS) - tamanho)},{'task':errors}]) ,200, {'ContentType':'application/json'} 





@bp_task.route('/state/<string:id>', methods=['GET'])
def get_state(id):
    task = Task.objects(id_=id).first()
    if not task:
        return jsonify([])
    else:
        return task.to_json(),200, {'ContentType':'application/json'} 


@bp_task.route('/update', methods=['POST'])
def update_record():
    record = request.json
    task = Task.objects(id_=record['id_']).first()
    if not task:
        return jsonify({'error': 'data not found'})
    else:
        state = record['state']
        task_id = record['task_id']
        client = record['client']
        task.update(
            state = type_process(state),
            task_id = task_id,
            client = client)
        current_app.logger.warning(f'Update na Task: {task_id}')
    return task.to_json()


@bp_task.route('/add', methods=['POST'])
def add():
    record = request.json
    # {'version': 'V001', 'name': '2019', 'state': 'None', 'task_id': 'None'}
    task = Task(id_=id_(
        record['version'],
        record['name']),
        **record)
    task.save()
    return jsonify(task.to_json())


