import streamlit as st
import requests


def scraping_xal(name):
    post_url = "http://localhost:5050/scrapingmarketin"
    post_data = name
    try:

        response = requests.post(post_url,
                                 json=post_data)  # Αποστολή ονόματος του προϊόντος στο b-end και αναμονή για λήψη απάντησης απο το APIμε POST
        if response.status_code == 200:

            return response.json()  # Επιστροφή αποτελεσμάτων στο UI (Τιμή, εικόνα και περιγραφή από Χαλκιαδάκη)
        else:
            return "Δεν είναι δυνατή η πραγματοποίηση του αιτήματος", response.status_code

    except Exception as e:
        print(f"Connection failed: {e}")


name = "DOLE Μπανάνα"
results=scraping_xal(name)
print(results["name"])
print(results["url"])