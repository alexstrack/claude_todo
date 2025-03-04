from flask_smorest import Api


def init_api(app):
    api = Api(app)
    
    from api.resources.tasks import blp as TaskBlueprint
    
    api.register_blueprint(TaskBlueprint)