from typing import List

import streamlit as st

from util.config_loader import load_products_from_json
from util.Product import Product


def setup_state_variables():

    if "product_list" not in st.session_state:
        st.session_state["product_list"] = load_products_from_json(
            "config/products.json"
        )

    if "order" not in st.session_state:
        st.session_state["order"] = {"products": {}}


def setup_streamlit_app():

    st.set_page_config(
        page_title="Packing Dashboard",
        page_icon="📦",
        initial_sidebar_state="collapsed",
        layout="wide"
    )

    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    hide_streamlit_style = """
                <style>
                # MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def is_product_in_order(product: Product):
    order = st.session_state["order"]
    for order_product_id in order["products"].keys():
        if order_product_id == product.id:
            return True
    return False


def is_product_not_in_order(product: Product):
    return not is_product_in_order(product)


def get_products_not_in_order() -> List[Product]:
    products = st.session_state["product_list"]
    unused_products = filter(is_product_not_in_order, products)
    return unused_products


def update_product(old_product, new_product, amount):
    print(f"old: {old_product.id}, new: {new_product.id}")
    del st.session_state["order"]["products"][old_product.id]
    st.session_state["order"]["products"][new_product.id] = {
        "product": new_product,
        "amount": amount}

    print(st.session_state["order"]["products"])


def update_amount(product, new_amount):
    products = st.session_state["order"]["products"].copy()
    products[product.id]["amount"] = new_amount
    st.session_state["order"]["products"] = products
    print("new amount: ", new_amount)
    print("new state: ", st.session_state["order"]["products"])


def draw_order_product_editor():

    products = st.session_state["order"]["products"].copy()
    print("draw state: ", st.session_state["order"]["products"])

    for key in products.keys():
        item = products[key]
        product = item["product"]
        amount = item["amount"]

        with st.expander(f"{product.name} ({amount} pieces)", expanded=True):
            c1, c2 = st.columns([5, 5])

            possible_products = list(get_products_not_in_order())
            possible_products.append(product)
            possible_products_dict = {}
            for p in possible_products:
                possible_products_dict[f"{p.name} ({p.id})"] = p

            selected_product = c1.selectbox(
                key=f"selectbox_{key}",
                label="change product",
                index=possible_products.index(product),
                options=possible_products_dict.keys(),
                on_change=lambda: update_product(
                    old_product=product,
                    new_product=possible_products_dict[selected_product],
                    amount=amount
                ))

            selected_amount = c2.number_input(
                key=f"number_input_{key}",
                label="change amount",
                value=amount)

            if (selected_amount != amount):
                update_amount(product=product, new_amount=selected_amount)
