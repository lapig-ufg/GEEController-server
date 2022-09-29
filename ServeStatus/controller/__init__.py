from ServeStatus.app.controller.config import bp_config
from ServeStatus.app.controller.task import bp_task
from ServeStatus.app.controller.coder import bp_coder


def init_app(app):
    app.register_blueprint(bp_config)
    app.register_blueprint(bp_task)
    app.register_blueprint(bp_coder)