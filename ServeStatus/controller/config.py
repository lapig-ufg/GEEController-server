from flask import Blueprint, current_app, request, jsonify
from ServeStatus.model import Task
from ServeStatus.model import Config
from ServeStatus.Lapig.Functions import type_process, id_
from dynaconf import settings
from sys import exit





bp_config = Blueprint('config', __name__,url_prefix ='/config')


@bp_config.route('/generate_task_list', methods=['GET'])
def generate_task_list():
    try:
        queue = []
        for n,i in enumerate(settings.LIST_OF_TASKS):
            rest = {
                    'version':settings.VERSION,
                    'name':str(i),
                    'state':type_process('None'),
                    'task_id':'None',
                    'num':n,
                    'client': ''
                }
            my_id = id_(rest['version'], rest['name'])
            if Task.objects(id_=my_id).first():
                current_app.logger.warning(f'Task já existe {id_(rest["version"],rest["name"])}')
            else:
                task = Task(id_=my_id, **rest)
                task.save()
                rest['id_'] = my_id
                queue.append(rest)
                current_app.logger.warning(f'Add {rest}')
        return jsonify([
            {
                'state':'sucesso',
                'len_add_in_queue':len(queue)
            },
            {
                'add_in_queue':queue
                }
        ]),201
    except Exception as e:
        return jsonify([{
            'state':'error',
            'error': str(e) ,
            'messagem':'Erro a gerar a lista'}])
