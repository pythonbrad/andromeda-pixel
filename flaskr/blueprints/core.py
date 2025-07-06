from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    current_app,
)
from werkzeug.utils import secure_filename
import os


bp = Blueprint("core", __name__, url_prefix="/")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]
    )


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/upload_image", methods=["GET", "POST"])
def upload_image():
    if request.method != "POST":
        return redirect(url_for("core.index"))

    if "image" not in request.files:
        flash("We haven't receive your image!", "danger")

        return redirect(url_for("core.index"))

    keywords = request.args.get("keywords", "")
    file = request.files["image"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("Your image seems invalid!", "warning")
    elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config["MEDIA_ROOT"], filename))

        with open(current_app.config["MEDIA_ROOT"] / (filename + ".txt"), "w") as f:
            f.write(keywords)

        flash("Image uploaded successfully!", "success")

    return redirect(url_for("core.index"))


# Serve the media files.
@bp.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(current_app.config["MEDIA_ROOT"], name)
