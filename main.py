import streamlit as st
import requests
from app import ai_prompt
from app.ai_prompt import post_cart

# Mock προϊόντα
products = [
    {"name": "Γάλα", "category": "Τρόφιμα", "price": 1.5},
    {"name": "Τυρί", "category": "Τρόφιμα", "price": 3.2},
    {"name": "Ψωμί", "category": "Τρόφιμα", "price": 1.0},
    {"name": "Καφές", "category": "Ροφήματα", "price": 4.0},
    {"name": "Χυμός Πορτοκάλι", "category": "Ροφήματα", "price": 2.5},
    {"name": "Ζάχαρη", "category": "Είδη Σπιτιού", "price": 1.2},
    {"name": "Αλεύρι", "category": "Είδη Σπιτιού", "price": 1.8},
    {"name": "Μπανάνα", "category": "Φρούτα", "price": 0.6},
    {"name": "Μήλο", "category": "Φρούτα", "price": 0.7},
]

 #Αντικατάσταση μοκ με πραγματικα δεδομενα απο mongo
try:
    response = requests.get("http://localhost:5000/products")
    if response.status_code == 200:
        products = response.json()
    else:
        st.error("❌ Σφάλμα κατά τη λήψη των προϊόντων από το backend.")
        products = []
except Exception as e:
    st.error(f"⚠️ Το backend δεν είναι διαθέσιμο: {e}")
    products = []

# Αρχικοποίηση καλαθιού
if "cart" not in st.session_state:  # session για να αποθηκεύουμε το καλάθι
    st.session_state.cart = {}

st.title("🛒 SmartCart - UnipiShop")

st.header("🔍Φίλτρα Αναζήτησης")

#Κατηγορίες προϊόντων
categories = list(set([p["category"] for p in products]))
categories.sort()
categories.insert(0, "Όλες")

# Επιλογή φίλτρων
selected_category = st.selectbox("Φίλτρο κατηγορίας:", categories)
search_query = st.text_input("Αναζήτηση προϊόντος:")
sort_option = st.selectbox("Ταξινόμηση:", ["Χωρίς ταξινόμηση", "Αλφαβητικά (Α-Ω)", "Αλφαβητικά (Ω-Α)", "Τιμή (αύξουσα)", "Τιμή (φθίνουσα)"])

# Εφαρμογή φίλτρων
filtered_products = products

# Φίλτρο κατηγορίας
if selected_category != "Όλες":
    filtered_products = [p for p in filtered_products if p["category"] == selected_category]

# Φίλτρο λέξης
if search_query:
    filtered_products = [p for p in filtered_products if search_query.lower() in p["name"].lower()]

# Ταξινόμηση
if sort_option == "Αλφαβητικά (Α-Ω)":
    filtered_products = sorted(filtered_products, key=lambda x: x["name"])
elif sort_option == "Αλφαβητικά (Ω-Α)":
    filtered_products = sorted(filtered_products, key=lambda x: x["name"], reverse=True)
elif sort_option == "Τιμή (αύξουσα)":
    filtered_products = sorted(filtered_products, key=lambda x: x["price"])
elif sort_option == "Τιμή (φθίνουσα)":
    filtered_products = sorted(filtered_products, key=lambda x: x["price"], reverse=True)

# Κενό πριν την εμφάνιση προϊόντων
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.subheader("🛍️ Προϊόντα προς επιλογή")


    # Προϊόντα και ποσότητες
for idx, product in enumerate(filtered_products):
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{product['name']}** — *{product['category']}*")
            st.markdown(f"💶 Τιμή: **{product['price']} €**")
        with col2:
            qty = st.number_input(
                f"Ποσότητα", min_value=1, max_value=10, step=1, key=f"qty_{idx}"
            )
            if st.button("Προσθήκη", key=f"add_{idx}"):   #κουμπι προσθήκη στο καλάθι
                pname = product["name"]
                if pname in st.session_state.cart: # Αν υπάρχει ήδη αυξάνεται η ποσότητ
                    st.session_state.cart[pname]["qty"] += qty
                else:
                    st.session_state.cart[pname] = {"qty": qty,"price": product["price"],"category": product["category"]}
                st.success(f"✅ Προστέθηκαν {qty} τεμάχια από το {pname}")


# Διαχωριστικό πριν το καλάθι
st.divider()
st.subheader("🧺 Το καλάθι μου")

if st.session_state.cart:
    total = 0
    remove_keys = []  # Αυτά θα αφαιρεθούν

    for name, item in st.session_state.cart.items():
        subtotal = item["qty"] * item["price"]  # Ενδιάμεσο σύνολο

        col1, col2 = st.columns([4, 1])  # 2 στήλες: για κείμενο & κουμπί

        with col1:   # Όνομα, κατηγορία, ποσότητα
            st.markdown(f"**{name}**<br><small>{item['qty']} τεμ.</small>", unsafe_allow_html=True)
        with col2:  # Κουμπί αφαίρεσης προϊόντος
            st.markdown(f"<span style='color:green'><b>{item['price']} €</b></span>", unsafe_allow_html=True)
            if st.button(f"❌", key=f"remove_{name}"):
                remove_keys.append(name)

        total += subtotal  # Συνολικό άθροισμα

    # Διαγραφή προϊόντων που πατήθηκαν
    for key in remove_keys:
        del st.session_state.cart[key]

    st.write(f"**Σύνολο: {total:.2f} €**")

    # Κουμπί ολοκλήρωσης αγοράς
    from datetime import datetime

    if st.button("Ολοκλήρωση αγοράς"):
        try:
            purchase = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "items": st.session_state.cart.copy()
            }
            response = requests.post("http://localhost:5000/purchase", json=purchase)
            if response.status_code == 200:
                st.success("🧾 Η αγορά ολοκληρώθηκε και καταχωρήθηκε!")
                st.session_state.cart.clear()
            else:
                st.error("❌ Η αποστολή της αγοράς απέτυχε.")
        except Exception as e:
            st.error(f"⚠️ Δεν μπόρεσα να συνδεθώ με το backend: {e}")

# cart=[{"name":"Μακαρόνια ΜΙΣΚΟ"},{"name":"Σάλτσα βασιλικός-τομάτα"}]

post_cart(products)

