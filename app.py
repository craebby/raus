from flask import Flask, render_template, request, redirect
from database import get_db_version, get_item, init_db, add_item, get_today_count, get_items, update_item

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
    quantity = int(request.form["quantity"])

    if name:
        add_item(quantity, name, action)

    return redirect("/")



@app.route("/save/<int:item_id>", methods=["POST"])
def save(item_id):
    name = request.form["name"].strip()
    action = request.form["action"]
    quantity = int(request.form["quantity"])

    if name:
        update_item(item_id, quantity, name, action)

    return redirect("/")


@app.route("/edit/<int:item_id>", methods=["GET"])
def edit(item_id):
    edit_item = get_item(item_id)
    print(edit_item)
    return render_template(
        "index.html",
        edit_item=edit_item,
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
