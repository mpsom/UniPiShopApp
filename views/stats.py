import streamlit as st
import matplotlib.pyplot as plt
from collections import defaultdict


# Γραφήματα στατιστικών προϊόντων

def render_stats():
    st.divider()
    st.subheader("📈 Γράφημα: Συχνότητα Προϊόντων σε Όλες τις Αγορές")

    product_counts = defaultdict(int)  # Υπολογισμός συνολικών ποσοτήτων για κάθε προϊόν
    for entry in st.session_state.history:
        for name, item in entry["items"].items():
            product_counts[name] += item["qty"]

    if product_counts:  # Δημιουργία του bar chart
        fig, ax = plt.subplots()
        ax.bar(product_counts.keys(), product_counts.values())
        ax.set_xlabel("Προϊόντα")
        ax.set_ylabel("Συνολική Ποσότητα")
        ax.set_title("Προϊόντα που αγοράστηκαν περισσότερο")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("Δεν υπάρχουν αγορές για ανάλυση.")

    # developer mode
    if st.session_state.get("debug_mode"):
        st.divider()
        st.subheader("📊 Στατιστικά (Developer Only)")

        # Συγκεντρωτικά στοιχεία προϊόντων από το ιστορικό
        product_totals = {}
        for purchase in st.session_state.history:
            for name, item in purchase["items"].items():
                product_totals[name] = product_totals.get(name, 0) + item["qty"]

        if product_totals:
            fig, ax = plt.subplots()
            ax.bar(product_totals.keys(), product_totals.values())
            ax.set_title("Συνολικές Αγορές ανά Προϊόν")
            ax.set_ylabel("Ποσότητα")
            ax.set_xticklabels(product_totals.keys(), rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.info("Δεν υπάρχουν δεδομένα για προβολή γραφήματος.")
