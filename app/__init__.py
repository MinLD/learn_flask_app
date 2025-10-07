# app/__init__.py

from flask import Flask , jsonify

from .extensions import db, migrate, jwt
from config import config
from .models.models_model import User, TokenBlocklist
import cloudinary


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.json.sort_keys = False
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )


    from .controller.auth_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from .controller.users_controller import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    from .controller.organization_controller import organization_bp
    app.register_blueprint(organization_bp, url_prefix='/organization')
    from .controller.challenges_controller import challenges_bp
    app.register_blueprint(challenges_bp, url_prefix='/challenges')
    from .controller.upload_controller import upload_bp
    app.register_blueprint(upload_bp, url_prefix='/upload')
    from .controller.organization_events_controller import organization_events_bp
    app.register_blueprint(organization_events_bp, url_prefix='/organization_events')
    


    # check_if_token_in_blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_data):
        jti = jwt_data["jti"]
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    #load user
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    #additional clams

    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        
        if identity == "admin":
            return {'is_admin': True}
        return {'is_admin': False}


    # jwt error handler
    @jwt.expired_token_loader
    def expered_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "The token has expired", "error": "token_expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):  
        return jsonify({
            "description": "Request does not contain an access token.",
            "error": "authorization_required"
        }), 401

    
    from .models import models_model
    from .services import users_service, auth_service, role_service, organization_service, challenges_service, upload_service
    return app