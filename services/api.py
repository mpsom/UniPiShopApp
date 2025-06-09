import requests

BACKEND_URL = "http://127.0.0.1:5050"

def get_all_products():
    try:
        res = requests.get(f"{BACKEND_URL}/getallproducts")
        return res.json() if res.status_code == 200 else []
    except Exception as e:
        return []

def update_product(product):
    return requests.put(f"{BACKEND_URL}/updateproduct", json=product)

def delete_product(product_id):
    return requests.delete(f"{BACKEND_URL}/deleteproduct/{product_id}")

def add_product(product):
    return requests.post(f"{BACKEND_URL}/insertproduct", json=product)

def send_purchase(purchase):
    try:
        res = requests.post(f"{BACKEND_URL}/purchase", json=purchase)
        return res.status_code == 200
    except:
        return False

def send_to_ai(cart):
    try:
        res = requests.post(f"{BACKEND_URL}/finalcart", json=cart)
        if res.status_code == 200:
            return res.json()
        return None
    except:
        return None
