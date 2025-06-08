import streamlit as st
import requests


def scraping_markin(name):
    post_url = "http://localhost:5050/scrapingbazaar"
    post_data = name
    try:

        response = requests.post(post_url,
                                 json=post_data)  # Αποστολή ονόματος του προϊόντος στο b-end και αναμονή για λήψη απάντησης από το API με POST
        if response.status_code == 200:
            data = response.json()
            image = data['Εικόνα']
            price = data['Τιμή']
            description = data['Περιγραφή']
            return image, price, description  # Επιστροφή αποτελεσμάτων στο UI (tιμή, εικόνα και περιγραφή από MarketIn)
        else:
            return "Δεν είναι δυνατή η πραγματοποίηση του αιτήματος", response.status_code

    except Exception as e:
        print(f"Connection failed: {e}")
