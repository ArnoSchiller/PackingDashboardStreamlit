import streamlit as st

from util.streamlit_helper import *

setup_streamlit_app()

setup_state_variables()

content = st.container()
orderEditorContainer, _, packingEditorContainer = content.columns([3, 1, 6])


def clear_order():
    st.session_state["order"] = {"products": {}}
    st.session_state["order_changed"] = True


def add_new_product(product: Product):
    st.session_state["order"]["products"][product.id] = {
        "product": product, "amount": 1}
    st.session_state["order_changed"] = True


def trigger_packing():
    st.session_state["order_changed"] = False


with orderEditorContainer:
    st.subheader("Order list editor")
    draw_order_product_editor()
    st.markdown("-----")

possible_products_dict = get_products_not_in_order_dict()
if len(possible_products_dict.keys()) > 0:
    c1, c2 = orderEditorContainer.columns([7, 3])

    selected_product_key = c1.selectbox(
        key=f"selectbox_product",
        label="select product",
        label_visibility="collapsed",
        options=possible_products_dict.keys()
    )
    c2.button(
        label="add ➕",
        on_click=lambda: add_new_product(
            possible_products_dict[selected_product_key]),
        use_container_width=True)

orderEditorContainer.button(label="clear order ❌", on_click=clear_order)

if st.session_state["order_changed"]:
    packingEditorContainer.info(
        "The order has been updated, do you want to reload the packing?", icon="ℹ️")

packingEditorContainer.button(
    label="reload",
    disabled=not st.session_state["order_changed"],
    on_click=trigger_packing)

if not st.session_state["order_changed"]:
    packingEditorContainer.write(st.session_state["order"])
