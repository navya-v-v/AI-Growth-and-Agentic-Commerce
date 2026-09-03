import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="AgentCart AI",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 AgentCart AI")
st.subheader("Your Intelligent AI Shopping Agent")

st.write(
    "Tell me what you want to buy, and AgentCart AI "
    "will help you find suitable products."
)

user_request = st.text_area(
    "What are you looking for?",
    placeholder="Example: I need a laptop under ₹60,000 for coding and AI/ML"
)

if st.button("🤖 Ask Agent"):

    if user_request.strip():

        st.success("Your request has been received!")

        st.write("### Your requirement")
        st.write(user_request)

    else:

        st.warning("Please enter your requirement.")
