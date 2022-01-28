
from flask import Flask, jsonify, redirect
import os
from src.auth import auth
from src.constants.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.scholarship_posts import scholarships_blueprint
from src.Models import db, ScholarshipPost
# from flask_jwt_extended import JWTMangaer
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),

            SWAGGER={
                'title': 'SCHOLARSHUB API',
                'uiversion': 3,

            }
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(scholarships_blueprint)

    Swagger(app, config=swagger_config, template=template)

    @app.get('/<short_url>')
    @swag_from('./docs/short_url.yaml')
    def redirect_to_url(short_url):
        scholarShipPost = ScholarshipPost.query.filter_by(
            app_short_url=short_url).first_or_404()

        if scholarShipPost:
            scholarShipPost.visits = scholarShipPost.visits+1
            db.session.commit()

            return redirect(scholarShipPost.app_url)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            'error': 'Not found'
        }), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({
            'error': 'Internal server error, please check back'
        }), HTTP_500_INTERNAL_SERVER_ERROR
    return app
