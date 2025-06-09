import streamlit as st
from views.filters import render_filters
from views.product_list import render_product_list
from views.cart import render_cart
from views.purchase import render_purchase_section
from views.history import render_purchase_history
from views.stats import render_stats
from services.api import get_all_products

#devmode
dev_mode = st.sidebar.checkbox ("Developer Mode")

# Εκκίνηση εφαρμογής
st.title("🛒 SmartCart - UnipiShop")

# Φόρτωση προιοντων από το backend
products = get_all_products()

# Αρχικοποιηση state
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "history" not in st.session_state:
    st.session_state.history = []

# Φίλτρα προϊόντων
filtered_products = render_filters(products)

# Προβολή προϊόντων με δυνατότητα προσθήκης στο καλάθι
render_product_list(filtered_products)

# Εμφάνιση καλαθιού και δυνατότητα αγοράς
render_cart()
render_purchase_section()

# Ιστορικό αγορών
render_purchase_history()

# Γραφήματα και στατιστικά
render_stats()


if dev_mode:
    from views.developer import render_developer
    render_developer()
