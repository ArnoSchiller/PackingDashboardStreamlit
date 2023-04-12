import streamlit as st

from util.streamlit_helper import *

setup_streamlit_app()

setup_state_variables()

orderEditorContainer, _, packingEditorContainer = st.columns([3, 1, 6])


def clear_order():
    st.session_state["order"] = {"products": {}}


def add_new_product_selector():
    products = list(get_products_not_in_order())
    print(products)
    if len(products) < 1:
        return
    product = products[0]
    st.session_state["order"]["products"][product.id] = {
        "product": product, "amount": 1}


with orderEditorContainer:
    st.subheader("Order list editor")
    st.write(st.session_state["order"]["products"])
    draw_order_product_editor()

orderEditorContainer.button(label="add new product",
                            on_click=add_new_product_selector)
orderEditorContainer.button(label="clear order ❌", on_click=clear_order)

packingEditorContainer.write("Hello")
