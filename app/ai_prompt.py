import streamlit as st
import requests


def post_cart(cart):
    post_url = "http://127.0.0.1:5050/finalcart"
    post_data = cart
    try:
        response = requests.post(post_url, json=post_data)
        if response.status_code == 200:
            return "POST Request Successful", response.status_code
        else:
            return "POST Request Failed", response.status_code

    except Exception as e:
        print(f"Connection failed: {e}")


products = [
    {"name": "Σαλτσα barilla με βασιλικο", "category": "Τρόφιμα", "price": 1.5},
    {"name": "Τυρί", "category": "Τρόφιμα", "price": 3.2},
   # {"name": "Ψωμί", "category": "Τρόφιμα", "price": 1.0},
    {"name": "Μακαρονια", "category": "Ροφήματα", "price": 4.0},
    # {"name": "Χυμός Πορτοκάλι", "category": "Ροφήματα", "price": 2.5},
    # {"name": "Ζάχαρη", "category": "Είδη Σπιτιού", "price": 1.2},
    # {"name": "Αλεύρι", "category": "Είδη Σπιτιού", "price": 1.8},
    # {"name": "Μπανάνα", "category": "Φρούτα", "price": 0.6},
    # {"name": "Μήλο", "category": "Φρούτα", "price": 0.7},
]

post_cart(products)
response = requests.post("http://127.0.0.1:5050/finalcart", json=products)
if response.status_code == 200:
    aiprompt = response.json()
    print(aiprompt)
else:
    print("Connection Failed")
