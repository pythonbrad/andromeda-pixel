from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    session,
)
from werkzeug.utils import secure_filename
import random
import os
import pathlib

# Configuration
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "secret")
app.config["MEDIA_ROOT"] = pathlib.Path(os.path.dirname(__file__)) / "media"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = {"png", "jpg", "jpeg"}
app.config["MAX_CONTENT_LENGTH"] = 1 * 1000 * 1000  # 1MB

# Ensure the media folder is existing.
pathlib.Path(app.config["MEDIA_ROOT"]).mkdir(exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_IMAGE_EXTENSIONS"]
    )


def load_images():
    for file in pathlib.Path(app.config["MEDIA_ROOT"]).iterdir():
        if file.suffix == ".txt":
            continue

        with open(str(file.absolute()) + ".txt", "r") as f:
            keywords = f.read()

        yield {
            "url": url_for("download_file", name=file.name),
            "keywords": keywords,
            "uid": random.random(),
        }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload_image", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        flash("There is an error with your image!", "danger")

        return redirect(url_for("index"))

    keywords = request.args.get("keywords", "")
    file = request.files["image"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file!", "warning")
    elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_ROOT"], filename))

        with open(app.config["MEDIA_ROOT"] / (filename + ".txt"), "w") as f:
            f.write(keywords)

        flash("Image uploaded successfully!", "success")

    return redirect(url_for("index"))


# Serve the media files.
@app.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(app.config["MEDIA_ROOT"], name)


@app.route("/htmx/search")
def htmx_search():
    # We reset the pagination.
    session["skip"] = 0
    session["keywords"] = request.args.get("keywords", "")

    return render_template("gallery.html")


@app.route("/htmx/gallery")
def htmx_gallery():
    skip = session.get("skip", 0)
    keywords = session.get("keywords", "")
    images = load_images()
    counter = 0

    # Skip already readed data
    for i in range(skip):
        if not next(images, None):
            break

    # We load images in batch of 04.
    selected_images = []
    while image := next(images, None):
        # Filter per keywords
        detection = [k in image["keywords"] for k in keywords.split(" ")]
        if not any(detection):
            continue

        counter += 1

        selected_images.append(image)
        if counter == 4:
            break

    # We prepare the next pagination.
    session["skip"] = skip + counter

    return render_template("images.html", images=selected_images)


@app.route("/htmx/upload_image")
def htmx_upload_image():
    return render_template("upload_image.html")
