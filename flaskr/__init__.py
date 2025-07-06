from flask import Flask
import os
import pathlib


def create_app(test_config=None):
    # Configuration
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        MAX_CONTENT_LENGTH=1 * 1000 * 1000,  # 1MB
        MEDIA_ROOT=pathlib.Path(os.path.dirname(__file__)) / "media",
        ALLOWED_IMAGE_EXTENSIONS={"png", "jpg", "jpeg"},
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the media folder is existing.
    pathlib.Path(app.config["MEDIA_ROOT"]).mkdir(exist_ok=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .blueprints import core, htmx

    app.register_blueprint(htmx.bp)
    app.register_blueprint(core.bp)

    return app
