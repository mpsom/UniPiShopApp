import streamlit as st
import requests

# Εμφάνιση λίστας προϊόντων με δυνατότητα προσθήκης στο καλάθι
def render_product_list(filtered_products):
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    st.subheader("🛍️ Προϊόντα προς επιλογή")

 # Προϊόντα και ποσότητες
    for idx, product in enumerate(filtered_products):
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                try:
                    st.image("http://localhost:5050" + product["image"], width=100)
                except:
                    st.image("https://via.placeholder.com/100?text=No+Image", width=100)
                st.markdown(f"**{product['name']}** — *{product['category']}*")
                st.markdown(f"💶 Τιμή: **{product['price']} €**")
                st.markdown(f"📄 _{product['description']}_")
            with col2:
                qty = st.number_input("Ποσότητα", min_value=1, max_value=10, step=1, key=f"qty_{idx}")
                if st.button("Προσθήκη", key=f"add_{idx}"):
                    pname = product["name"]
                    if pname in st.session_state.cart:
                        st.session_state.cart[pname]["qty"] += qty
                    else:
                        st.session_state.cart[pname] = {
                            "qty": qty,
                            "price": product["price"],
                            "category": product["category"]
                        }
                    st.success(f"✅ Προστέθηκαν {qty} τεμάχια από το {pname}")

                    # Ενημέρωση backend->ΒΔ

                    try:
                        requests.put("http://localhost:5050/updatecart", json={
                            "product_name": pname,
                            "product": st.session_state.cart[pname]
                        })  # 🔴
                    except Exception as e:
                        st.error(f"⚠️ Αποτυχία ενημέρωσης καλαθιού στο backend: {e}")
