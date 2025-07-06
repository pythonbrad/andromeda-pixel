from flask import Flask
import os


def create_app(test_config=None):
    # Configuration
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        MAX_CONTENT_LENGTH=2_000_000,
        AWS_S3_BUCKET_NAME="dev",
        ALLOWED_IMAGE_EXTENSIONS={"png", "jpg", "jpeg"},
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    from .blueprints import core, htmx

    app.register_blueprint(htmx.bp)
    app.register_blueprint(core.bp)

    return app
