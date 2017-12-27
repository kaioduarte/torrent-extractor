from re import match
from flask import (
    Flask,
    render_template,
    request,
    redirect
)

from scrape import get_torrents


app = Flask(__name__)
app.config.from_pyfile("config.py")


@app.route("/", methods=["GET"])
def index():
  return render_template("index.html")


@app.errorhandler(404)
def error(e):
  return redirect("/")


def validate_args(args: dict) -> bool:
  if {"url"} != args.to_dict().keys():
    return False
  else:
    url_match = match(r"https?://w{3}.*", args.get("url"))
    return url_match is not None


@app.route("/extract", methods=["GET"])
def search():
  if not validate_args(request.args):
    return redirect("/")
  else:
    links = get_torrents(request.args.get("url"))
    return render_template("links.html", links=links)


if __name__ == '__main__':
  app.run(
      debug=app.config["DEBUG"]
  )
