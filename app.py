from flask import Flask, render_template, request, redirect
from database import init_db, add_item, get_today_count, get_items

app = Flask(__name__)

init_db()


@app.route("/")
def index():
    today_count = get_today_count()
    items = get_items()

    return render_template(
        "index.html",
        today_count=today_count,
        items=items,
    )


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"].strip()
    action = request.form["action"]

    if name:
        add_item(name, action)

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
