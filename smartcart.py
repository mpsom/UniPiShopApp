import streamlit as st
from services.api import get_all_products
from views.filters import render_filters
from views.product_list import render_product_list
from views.cart import render_cart
from views.purchase import render_purchase_section
from views.history import render_purchase_history
import requests

# Developer Mode
dev_mode = st.sidebar.checkbox("Developer Mode")

# Αν ο χρήστης είναι Developer
if dev_mode:
    # Εμφάνιση του Developer Panel
    from views.developer import render_developer

    render_developer()

# Αν ο χρήστης είναι "Κανονικός Χρήστης"
else:
    st.title("🛒 SmartCart - UnipiShop")

    # Φόρτωση προϊόντων από το backend
    products = get_all_products()

    # Αρχικοποίηση session state για καλάθι και ιστορικό
    if "cart" not in st.session_state:
        try:
            res = requests.get("http://localhost:5050/getcart")
            if res.status_code == 200:
                st.session_state.cart = res.json()
            else:
                st.session_state.cart = {}
        except Exception as e:
            st.session_state.cart = {}

    if "history" not in st.session_state:
        st.session_state.history = []

    filtered_products = render_filters(products)  # Εμφάνιση φίλτρων
    render_product_list(filtered_products)  # Προβολή προϊόντων και δυνατότητα προσθήκης στο καλάθι
    render_cart()  # Εμφάνιση καλαθιού και κουμπιού ολοκλήρωσης αγοράς
    render_purchase_section()
    render_purchase_history()  # Εμφάνιση ιστορικού αγορών
