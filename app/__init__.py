from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_restful import Api, abort

from app.models.base import db
from app.resources.captcha import ResourceCaptcha
from app.resources.invitation_code import ResourceInvitationCode
from app.resources.node import ResourceNodeCSV, ResourceNodeDescription

cors = CORS(supports_credentials=True)
login_manager = LoginManager()


def create_app(test=False, file_directory=None):
    app = Flask(__name__)
    try:
        app.config.from_object("app.config")
    except ImportError:
        app.config.from_object("app.config_demo")
    if test:
        app.config["TESTING"] = True
        app.config["FILE_DIRECTORY"] = file_directory
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "sqlite:///../{}/.database?check_same_thread=False".format(file_directory)
    register_resource(app)
    register_plugin(app)
    return app


def register_plugin(app_):
    # 注册sqlalchemy
    db.init_app(app_)

    # 初始化数据库
    with app_.app_context():
        db.create_all()

    # 注册cors
    cors.init_app(app_)

    # 注册用户管理器
    from app.models.user import User

    @login_manager.user_loader
    def load_user(id_):
        return User.get_by_id(id_)

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        abort(401)

    login_manager.init_app(app_)

    return app_


def register_resource(app_):
    from app.resources.file import ResourceFile, ResourceFileDirectory
    from app.resources.node import (
        ResourceNode,
        ResourceNodeEdge,
        ResourceNodeList,
        ResourceNodeRun,
    )
    from app.resources.project import (
        ResourceProject,
        ResourceProjectList,
        ResourceProjectRun,
    )
    from app.resources.session import ResourceSession
    from app.resources.user import ResourceUser, ResourceUserList

    api = Api(catch_all_404s=True)
    api.add_resource(ResourceSession, "/session")
    api.add_resource(ResourceCaptcha, "/captcha")
    api.add_resource(ResourceInvitationCode, "/invitation_code")
    api.add_resource(ResourceUser, "/user/<int:id_>")
    api.add_resource(ResourceUserList, "/user")
    api.add_resource(ResourceProject, "/project/<int:id_>")
    api.add_resource(ResourceProjectList, "/project")
    api.add_resource(ResourceProjectRun, "/project/<int:id_>/run")
    api.add_resource(ResourceFile, "/file")
    api.add_resource(ResourceFileDirectory, "/file/directory")
    api.add_resource(ResourceNode, "/node/<int:id_>")
    api.add_resource(ResourceNodeList, "/node")
    api.add_resource(ResourceNodeEdge, "/node/edge")
    api.add_resource(ResourceNodeRun, "/node/<int:id_>/run")
    api.add_resource(ResourceNodeCSV, "/node/<int:id_>/csv")
    api.add_resource(ResourceNodeDescription, "/node/description")
    api.init_app(app_)
    return app_
