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

    if "order_changed" not in st.session_state:
        st.session_state["order_changed"] = False


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


def get_products_not_in_order_dict() -> dict:
    possible_products = list(get_products_not_in_order())
    possible_products_dict = {}
    for p in possible_products:
        possible_products_dict[f"{p.name} ({p.id})"] = p
    return possible_products_dict


def remove_product(product):
    del st.session_state["order"]["products"][product.id]
    st.session_state["order_changed"] = True


def update_amount(product, key):
    new_amount = st.session_state[f"number_input_{key}"]
    p = st.session_state["order"]["products"]
    st.session_state["order"]["products"][product.id]["amount"] = new_amount
    st.session_state["order_changed"] = True
    print(f"new_amount {new_amount}, state {p}")


def draw_order_product_editor():

    products = st.session_state["order"]["products"].copy()
    # print("draw state: ", st.session_state["order"]["products"])

    for key in products.keys():
        item = products[key]
        product = item["product"]
        amount = item["amount"]

        c1, c2, c3 = st.columns([5, 4, 2])

        c1.markdown(
            f"**{product.name}** ({product.id})")

        selected_amount = c2.number_input(
            key=f"number_input_{key}",
            label="input amount",
            label_visibility="collapsed",
            value=1,
            min_value=1,
            on_change=lambda: update_amount(product, key))

        c3.button(
            key=f"delete_button_{key}",
            label="❌",
            type="secondary",
            on_click=lambda: remove_product(product),
            use_container_width=True)
