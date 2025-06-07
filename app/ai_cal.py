import streamlit as st
import requests


# Επικοινωνία με το backend για την αποστολή του τελικού καλαθιού
def post_cart_and_get_aiprompt(cart):
    post_url = "http://127.0.0.1:5050/finalcart"
    post_data = cart
    try:

        response = requests.post(post_url, json=post_data)  # Αποστολή του τελικού καλαθιού στο b-end API με POST
        if response.status_code == 200:

            return response.json()  # Λήψη απάντησης του b-end (AI απάντηση σε json)
        else:
            return "POST Request Failed", response.status_code

    except Exception as e:
        print(f"Connection failed: {e}")





products = [
    {"name": "Σαλτσα barilla με βασιλικο", "category": "Τρόφιμα", "price": 1.5},
    {"name": "Τυρί", "category": "Τρόφιμα", "price": 3.2},
    # {"name": "Ψωμί", "category": "Τρόφιμα", "price": 1.0},
    {"name": "Μακαρονια", "category": "Ροφήματα", "price": 4.0}, ]
ai_response=post_cart_and_get_aiprompt(products)
for obj in ai_response:
    for key, value in obj.items():
        print(f"---\n**{key}:**\n\n{value}")
