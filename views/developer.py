import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from services.api import (
    get_all_products, update_product, delete_product,
    add_product, scrape_bazaar, scrape_marktin, scrape_xal
)

# Developer Panel
def render_developer():
    st.title(" Developer Panel")

    # Δημιουργία δύο καρτελών: Διαχείριση Προϊόντων & Στατιστικά
    tab1, tab2, tab3 = st.tabs(["📦 Προϊόντα", "📊 Στατιστικά", "🔍 Σύγκριση Τιμών"])

    # --- TAB 1: Διαχείριση Προϊόντων ---
    with tab1:
        st.header("Διαχείριση Προϊόντων")
        products = get_all_products()  # Λήψη όλων των προϊόντων από το backend

        df = pd.DataFrame(products)
        st.dataframe(df)  # Προβολή σε πίνακα

        st.subheader("✏️ Ενημέρωση ή Διαγραφή Προϊόντος")
        selected = st.selectbox("Διάλεξε προϊόν:", products, format_func=lambda x: x["name"])

        #  Φόρμα ενημέρωσης επιλεγμένου προϊόντος
        name = st.text_input("Όνομα", value=selected["name"])
        category = st.text_input("Κατηγορία", value=selected["category"])
        subcategory = st.text_input("Υποκατηγορία", value=selected["subcategory"])
        price = st.number_input("Τιμή", value=selected["price"], min_value=0.0, step=0.1)
        description = st.text_area("Περιγραφή", value=selected["description"])
        image = st.text_input("URL Εικόνας", value=selected["image"])

        if st.button("Αποθήκευση Αλλαγών"):
            update_product({
                "_id": selected["_id"], "name": name, "category": category,
                "subcategory": subcategory, "price": price,
                "description": description, "image": image
            })
            st.success("✅ Το προϊόν ενημερώθηκε.")

        if st.button("🗑️ Διαγραφή Προϊόντος"):
            delete_product(selected["_id"])
            st.warning("⚠️ Το προϊόν διαγράφηκε.")

        # ➕ Προσθήκη νέου προϊόντος
        st.subheader("➕ Προσθήκη Νέου Προϊόντος")
        new_name = st.text_input("Νέο Όνομα")
        new_cat = st.text_input("Κατηγορία")
        new_sub = st.text_input("Υποκατηγορία")
        new_price = st.number_input("Τιμή", min_value=0.0, step=0.1, key="new_price")
        new_desc = st.text_area("Περιγραφή")
        new_img = st.text_input("URL Εικόνας")

        if st.button("➕ Προσθήκη Προϊόντος"):
            add_product({
                "name": new_name, "category": new_cat, "subcategory": new_sub,
                "price": new_price, "description": new_desc, "image": new_img
            })
            st.success("✅ Το νέο προϊόν προστέθηκε!")

    # --- TAB 2: Στατιστικά ---
    with tab2:
        st.header("📈 Στατιστικά Αγορών")
        if "history" in st.session_state:
            product_counts = defaultdict(int)
            for entry in st.session_state.history:
                for name, item in entry["items"].items():
                    product_counts[name] += item["qty"]

            if product_counts:
                fig, ax = plt.subplots()
                ax.bar(product_counts.keys(), product_counts.values())
                ax.set_xlabel("Προϊόντα")
                ax.set_ylabel("Ποσότητα")
                ax.set_title("Προϊόντα που αγοράστηκαν περισσότερο")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info(" Δεν υπάρχουν ακόμα δεδομένα.")
        else:
            st.warning("Το ιστορικό αγορών δεν είναι διαθέσιμο.")

    # --- TAB 3: Σύγκριση Τιμών με scraping ---
    with tab3:
        st.header("🔍 Σύγκριση Προϊόντων σε Σούπερ Μάρκετ")
        product_name = st.text_input("Όνομα προϊόντος για αναζήτηση:")

        if st.button("🔎 Bazaar"):
            data = scrape_bazaar(product_name)
            if data:
                st.image(data["Εικόνα"])
                st.write(f"💶 Τιμή: {data['Τιμή']}")
                st.write(f"📝 Περιγραφή: {data['Περιγραφή']}")
            else:
                st.warning("❌ Δεν βρέθηκε προϊόν στο Bazaar.")

        if st.button("🔎 Market-In"):
            data = scrape_marktin(product_name)
            if data:
                st.image(data["Εικόνα"])
                st.write(f"💶 Τιμή: {data['Τιμή']}")
                st.write(f"📝 Περιγραφή: {data['Περιγραφή']}")
            else:
                st.warning("❌ Δεν βρέθηκε προϊόν στο Market-In.")

        # #if st.button("🔎 Χαλκιαδάκης"):
        #     data = scrape_xal(product_name)
        #     if data:
        #         st.write(f"🔗 URL: {data['url']}")
        #     else:
        #         st.warning("❌ Δεν βρέθηκε προϊόν στο Χαλκιαδάκης.")
