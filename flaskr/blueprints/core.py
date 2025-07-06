from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from werkzeug.utils import secure_filename
from flaskr.db import get_db
import boto3
from boto3.s3.transfer import S3UploadFailedError
import tempfile
from PIL import Image, UnidentifiedImageError

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

    keywords = request.form.get("keywords", "")
    file = request.files["image"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "" or not (file and allowed_file(file.filename)):
        img_types = ", ".join(current_app.config["ALLOWED_IMAGE_EXTENSIONS"])
        flash(f"Sorry, but we only allow image types: {img_types}!", "warning")
    else:
        filename = secure_filename(file.filename)

        # Temporary save the file.
        tfile = tempfile.mktemp()
        file.save(tfile)

        # Check if the file is an image.
        try:
            im = Image.open(tfile)
            im_status = True
            im.close()
        except UnidentifiedImageError:
            im_status = False

        if not im_status:
            flash("Your image seems invalid!", "danger")

            return redirect(url_for("core.index"))

        # Upload to AWS S3 bucket.
        client = boto3.resource("s3")
        bucket = client.Bucket(current_app.config["AWS_S3_BUCKET_NAME"])
        bucket_obj = bucket.Object(filename)

        try:
            bucket_obj.upload_file(tfile)
        except S3UploadFailedError as err:
            flash(
                "We got an issue during the uploading of your image. Please try again!",
                "danger",
            )
            current_app.logger.error(
                f"Couldn't upload file {filename} to {bucket.name}\n{err}."
            )

            return redirect(url_for("core.index"))

        # Update the database.
        db = get_db()
        db.execute(
            "INSERT INTO image (keywords, bucket_name, object_key) VALUES (?, ?, ?)",
            (keywords, bucket.name, bucket_obj.key),
        )
        db.commit()

        flash("Image uploaded successfully!", "success")

    return redirect(url_for("core.index"))


@bp.errorhandler(413)
def uploaded_file_too_large(e):
    max_upload_size = round(current_app.config["MAX_CONTENT_LENGTH"] / 1_000_000, 2)
    flash(
        f"The image is too large for us to upload it! The maximun is {max_upload_size} MB",
        "danger",
    )

    return redirect(url_for("core.index"))
