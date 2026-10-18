import json
import os
from functools import wraps
from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")
ITEMS_FILE = os.path.join(BASE_DIR, "items.json")


def init_files():
    if not os.path.exists(USERS_FILE):
        default_users = {"admin": "1234", "student": "pass"}
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_users, f, indent=4)

    if not os.path.exists(ITEMS_FILE):
        default_items = {
            "1": {"id": 1, "name": "Laptop", "price": 1200, "color": "Silver", "weight": 1.5},
            "2": {"id": 2, "name": "Smartphone", "price": 800, "color": "Black", "weight": 0.2},
            "3": {"id": 3, "name": "Headphones", "price": 150, "color": "White", "weight": 0.3}
        }
        with open(ITEMS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_items, f, indent=4)


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        users = load_json(USERS_FILE)
        if not auth or users.get(auth.username) != auth.password:
            resp = jsonify({"error": "Authentication required"})
            resp.status_code = 401
            resp.headers["WWW-Authenticate"] = 'Basic realm="Catalog"'
            return resp
        return f(*args, **kwargs)
    return decorated


@app.route("/items", methods=["GET", "POST"])
@require_auth
def handle_items():
    items = load_json(ITEMS_FILE)

    if request.method == "GET":
        return jsonify(list(items.values())), 200

    if request.method == "POST":
        data = request.get_json()
        if not data or "name" not in data or "price" not in data:
            return jsonify({"error": "Invalid item data"}), 400

        new_id = str(data.get("id") or (max([int(k) for k in items.keys()], default=0) + 1))
        if new_id in items:
            return jsonify({"error": f"Item {new_id} already exists"}), 400

        new_item = {
            "id": int(new_id),
            "name": data["name"],
            "price": data["price"],
            "color": data.get("color", "Unknown"),
            "weight": data.get("weight", 0.0)
        }
        items[new_id] = new_item
        save_json(ITEMS_FILE, items)
        return jsonify(new_item), 201


@app.route("/items/<int:item_id>", methods=["GET", "PUT", "DELETE"])
@require_auth
def handle_single_item(item_id):
    items = load_json(ITEMS_FILE)
    str_id = str(item_id)

    if str_id not in items:
        return jsonify({"error": "Item not found"}), 404

    if request.method == "GET":
        return jsonify(items[str_id]), 200

    if request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        item = items[str_id]
        item["name"] = data.get("name", item["name"])
        item["price"] = data.get("price", item["price"])
        item["color"] = data.get("color", item["color"])
        item["weight"] = data.get("weight", item["weight"])

        items[str_id] = item
        save_json(ITEMS_FILE, items)
        return jsonify(item), 200

    if request.method == "DELETE":
        deleted = items.pop(str_id)
        save_json(ITEMS_FILE, items)
        return jsonify({"message": "Item deleted", "item": deleted}), 200


if __name__ == "__main__":
    init_files()
    app.run(host="127.0.0.1", port=8000)