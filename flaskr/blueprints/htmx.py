from flask import Blueprint, session, render_template, request
from flaskr.db import get_db
import boto3


bp = Blueprint("htmx", __name__, url_prefix="/htmx")


@bp.route("/search")
def search():
    # We reset the pagination.
    session["skip"] = 0
    session["keywords"] = request.args.get("keywords", "")

    return render_template("gallery.html")


@bp.route("/gallery")
def gallery():
    skip = session.get("skip", 0)

    # Filter
    cond_values = [f"%{keyword}%" for keyword in session.get("keywords", "").split(" ")]
    conds = " OR ".join(["keywords LIKE ?"] * len(cond_values))

    db = get_db()
    images = db.execute(
        f"SELECT * FROM image WHERE {conds} AND id > ? LIMIT ?", (*cond_values, skip, 4)
    ).fetchall()

    # Extract data from AWS S3.
    s3_client = boto3.client("s3")
    images = [
        {
            "url": s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": image["bucket_name"], "Key": image["object_key"]},
                ExpiresIn=3600,
            ),
            "keywords": image["keywords"],
        }
        for image in images
    ]

    # We prepare the next pagination.
    session["skip"] = skip + len(images)

    return render_template("images.html", images=images)


@bp.route("/upload_image")
def upload_image():
    return render_template("upload_image.html")
