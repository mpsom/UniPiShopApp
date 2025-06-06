import streamlit as st
import requests


# Επικοινωνία με το backend για την αποστολή του τελικού καλαθιού
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

        # Κλήση του backend για απάντηση από το API του ΑΙ

# def ai_answer:
# response = requests.post("http://127.0.0.1:5050/finalcart", json=cart)
#     if response.status_code == 200:
#         aiprompt = response.json()
#         for obj in aiprompt:
#             for key, value in obj.items():
#                 print(f"{key}:\n {value}")
#         else:
#             print("Connection Failed")



products = [
    {"name": "Σαλτσα barilla με βασιλικο", "category": "Τρόφιμα", "price": 1.5},
    {"name": "Τυρί", "category": "Τρόφιμα", "price": 3.2},
    # {"name": "Ψωμί", "category": "Τρόφιμα", "price": 1.0},
    {"name": "Μακαρονια", "category": "Ροφήματα", "price": 4.0}, ]
post_cart(products)
