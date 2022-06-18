from ServeStatus.controller.config import bp_config
from ServeStatus.controller.task import bp_task


def init_app(app):
    app.register_blueprint(bp_config)
    app.register_blueprint(bp_task)