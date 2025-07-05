from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/htmx/search")
def htmx_search():
    import time
    time.sleep(3)

    keywords = request.args.get('keywords', '')

    # TODO
    # We should filter and look for a way to pass the filter

    return render_template('gallery.html', keywords=keywords)

@app.route("/htmx/gallery")
def htmx_gallery():
    # TODO
    # save and increment the page for the next call
    images = [{
        "url":"https://bulma.io/assets/images/placeholders/256x256.png",
        "keywords": "blank galaxy",
        "author": "anonymous"
    }] * 4

    return render_template("images.html", images=images)

