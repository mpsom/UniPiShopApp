import streamlit as st
import requests

# Εμφάνιση περιεχομένων καλαθιού και δυνατότητα διαγραφής
def render_cart():
    st.divider()    # Διαχωριστικό πριν το καλάθι
    st.subheader("🧺 Το καλάθι μου")

    if not st.session_state.cart:
        st.info("Το καλάθι είναι άδειο.")
        return

    total = 0
    remove_keys =  []  # Αυτά θα αφαιρεθούν

    for name, item in st.session_state.cart.items():
        subtotal = item["qty"] * item["price"] # Ενδιάμεσο σύνολο
        col1, col2 = st.columns([4, 1]) # 2 στήλες: για κείμενο & κουμπί
        with col1:     # Όνομα, κατηγορία, ποσότητα
            st.markdown(f"**{name}**<br><small>{item['qty']} τεμ.</small>", unsafe_allow_html=True)
        with col2:     # Κουμπί αφαίρεσης προϊόντος
            st.markdown(f"<span style='color:green'><b>{item['price']} €</b></span>", unsafe_allow_html=True)
            if st.button("❌", key=f"remove_{name}"):
                remove_keys.append(name)
        total += subtotal    # Συνολικό άθροισμα

    # Διαγραφή προϊόντων που πατήθηκαν
    for key in remove_keys:
        del st.session_state.cart[key]
        try:
            requests.delete("http://localhost:5050/cart/deleteitem", json={
                "product_name": key
            })
        except Exception as e:
            st.error(f"⚠️ Αποτυχία διαγραφής στο backend: {e}")

    st.write(f"**Σύνολο: {total:.2f} €**")