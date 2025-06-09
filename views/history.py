import streamlit as st

# Προβολή ιστορικού αγορών

def render_purchase_history():
    st.divider()
    st.subheader("Ιστορικό Αγορών")

    if not st.session_state.history:
        st.info("Δεν υπάρχει ακόμη ιστορικό αγορών.")
        return

    for entry in reversed(st.session_state.history):   # Το πιο πρόσφατο πάνω
        st.markdown(f"**🕒 {entry['timestamp']}**")
        total = 0
        for name, item in entry["items"].items():
            subtotal = item["qty"] * item["price"]
            total += subtotal
            st.markdown(f"• {name} — {item['qty']} τεμ. × {item['price']} € = {subtotal:.2f} €")
        st.markdown(f"**Σύνολο: {total:.2f} €**")
        st.markdown("---")
