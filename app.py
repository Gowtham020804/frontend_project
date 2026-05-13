import streamlit as st
import pandas as pd
import numpy as np

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="FinSight",
    page_icon="💰",
    layout="wide"
)

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "signin"

if "user" not in st.session_state:
    st.session_state.user = ""

# ------------------------------------------------
# SIMPLE CSS
# ------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.main {
    background-color: #0E1117;
}

h1,h2,h3 {
    color: white;
}

.stButton>button {
    width: 100%;
    background-color: #5ce89b;
    color: black;
    border-radius: 10px;
    border: none;
    height: 45px;
    font-size: 16px;
    font-weight: bold;
}

.stTextInput>div>div>input {
    background-color: #1E1E1E;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIGN IN PAGE
# ------------------------------------------------
def signin_page():

    st.title("💰 FinSight")

    st.subheader("Sign In")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):

        if email and password:
            st.session_state.user = email
            st.session_state.page = "dashboard"
            st.rerun()

        else:
            st.error("Enter email and password")

    st.write("")

    if st.button("Continue with Google"):
        st.session_state.user = "Google User"
        st.session_state.page = "dashboard"
        st.rerun()

    st.write("---")

    st.write("Don't have an account?")

    if st.button("Create Account"):
        st.session_state.page = "signup"
        st.rerun()

# ------------------------------------------------
# SIGN UP PAGE
# ------------------------------------------------
def signup_page():

    st.title("📝 Create Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):

        if name and email and password:
            st.success("Account Created!")

            st.session_state.user = name
            st.session_state.page = "dashboard"
            st.rerun()

        else:
            st.error("Fill all fields")

    st.write("---")

    if st.button("Back to Sign In"):
        st.session_state.page = "signin"
        st.rerun()

# ------------------------------------------------
# DASHBOARD
# ------------------------------------------------
def dashboard_page():

    st.title("📊 Finance Dashboard")

    st.write(f"Welcome, {st.session_state.user}")

    # Sample data
    months = ["Jan", "Feb", "Mar", "Apr", "May"]

    income = [5000, 6200, 5800, 7100, 6900]

    expenses = [3200, 4100, 3900, 4500, 4300]

    df = pd.DataFrame({
        "Month": months,
        "Income": income,
        "Expenses": expenses
    })

    # Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("Income", "$31,000")
    col2.metric("Expenses", "$20,000")
    col3.metric("Profit", "$11,000")

    st.write("---")

    st.subheader("Income Chart")
    st.line_chart(df.set_index("Month")["Income"])

    st.subheader("Expense Chart")
    st.bar_chart(df.set_index("Month")["Expenses"])

    st.subheader("Financial Data")
    st.dataframe(df)

    st.write("---")

    if st.button("Logout"):
        st.session_state.page = "signin"
        st.rerun()

# ------------------------------------------------
# ROUTER
# ------------------------------------------------
if st.session_state.page == "signin":
    signin_page()

elif st.session_state.page == "signup":
    signup_page()

else:
    dashboard_page()
