from flask import Blueprint, session, render_template, request, current_app, url_for
import pathlib
import random


bp = Blueprint("htmx", __name__, url_prefix="/htmx")


def load_images():
    for file in pathlib.Path(current_app.config["MEDIA_ROOT"]).iterdir():
        if file.suffix == ".txt":
            continue

        with open(str(file.absolute()) + ".txt", "r") as f:
            keywords = f.read()

        yield {
            "url": url_for("core.download_file", name=file.name),
            "keywords": keywords,
            "uid": random.random(),
        }


@bp.route("/search")
def search():
    # We reset the pagination.
    session["skip"] = 0
    session["keywords"] = request.args.get("keywords", "")

    return render_template("gallery.html")


@bp.route("/gallery")
def gallery():
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


@bp.route("/upload_image")
def upload_image():
    return render_template("upload_image.html")
