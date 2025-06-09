import streamlit as st


def render_filters(products):
    categories = sorted(set(p["category"] for p in products))
    categories.insert(0, "Όλες")
    selected_category = st.selectbox("Φίλτρο κατηγορίας:", categories, key="category_select")

    # Αρχικοποίηση προϊόντων προς φιλτράρισμα
    filtered = products.copy()

    # Φίλτρο κατηγορίας
    if selected_category != "Όλες":
        filtered = [p for p in filtered if p["category"] == selected_category]
        subcategories = sorted(set(p["subcategory"] for p in filtered))
        subcategories.insert(0, "Όλες")
        selected_subcategory = st.selectbox("Φίλτρο υποκατηγορίας:", subcategories, key="subcategory_select")

        # Φίλτρο υποκατηγορίας
        if selected_subcategory != "Όλες":
            filtered = [p for p in filtered if p["subcategory"] == selected_subcategory]

    # Φίλτρο λέξης/Αναζήτηση
    search_query = st.text_input("Αναζήτηση προϊόντος:", key="search_input")
    if search_query:
        filtered = [p for p in filtered if search_query.lower() in p["name"].lower()]

    sort_option = st.selectbox("Ταξινόμηση:",
                               ["Χωρίς ταξινόμηση", "Αλφαβητικά (Α-Ω)", "Αλφαβητικά (Ω-Α)", "Τιμή (αύξουσα)",
                                "Τιμή (φθίνουσα)"],
                               key="sort_option")
    if sort_option == "Αλφαβητικά (Α-Ω)":
        filtered = sorted(filtered, key=lambda x: x["name"])
    elif sort_option == "Αλφαβητικά (Ω-Α)":
        filtered = sorted(filtered, key=lambda x: x["name"], reverse=True)
    elif sort_option == "Τιμή (αύξουσα)":
        filtered = sorted(filtered, key=lambda x: x["price"])
    elif sort_option == "Τιμή (φθίνουσα)":
        filtered = sorted(filtered, key=lambda x: x["price"], reverse=True)

    return filtered
