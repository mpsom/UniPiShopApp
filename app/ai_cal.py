import streamlit as st
import requests


# Επικοινωνία με το backend για την αποστολή του τελικού καλαθιού
def post_cart_and_get_aiprompt(cart):
    product_names = list(cart["items"].keys())
    cart_str = ", ".join(product_names)

    post_url = "http://127.0.0.1:5050/finalcart"
    post_data = cart_str
    try:

        response = requests.post(post_url,
                                 json=post_data)  # Αποστολή του τελικού καλαθιού στο b-end API με POST και αναμονή για απάντηση
        if response.status_code == 200:
            answers = response.json()
            recipe = answers["a1"]
            nutri_val = answers["a2"]
            return recipe, nutri_val
        else:
            return "Δεν είναι δυνατή η πραγματοποίηση του αιτήματος", response.status_code

    except Exception as e:
        print(f"Connection failed: {e}")
