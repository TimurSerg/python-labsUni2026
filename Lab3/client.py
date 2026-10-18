import requests

BASE_URL = "http://127.0.0.1:8000"
AUTH = ("admin", "1234")

r = requests.get(f"{BASE_URL}/items", auth=AUTH)
print("GET /items:", r.status_code, r.json())

new_product = {
    "name": "Gaming Mouse",
    "price": 75,
    "color": "RGB Black",
    "weight": 0.12
}
r = requests.post(f"{BASE_URL}/items", json=new_product, auth=AUTH)
created_item = r.json()
print("POST /items:", r.status_code, created_item)

item_id = created_item["id"]

r = requests.get(f"{BASE_URL}/items/{item_id}", auth=AUTH)
print(f"GET /items/{item_id}:", r.status_code, r.json())

update_data = {"price": 60, "color": "Matte Black"}
r = requests.put(f"{BASE_URL}/items/{item_id}", json=update_data, auth=AUTH)
print(f"PUT /items/{item_id}:", r.status_code, r.json())

r = requests.delete(f"{BASE_URL}/items/{item_id}", auth=AUTH)
print(f"DELETE /items/{item_id}:", r.status_code, r.json())

r = requests.get(f"{BASE_URL}/items", auth=AUTH)
print("GET /items:", r.status_code, r.json())