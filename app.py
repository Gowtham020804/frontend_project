import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Finance Dashboard",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Finance Dashboard")

st.write("Welcome to the Streamlit Finance App")

# Sample data
months = ["Jan", "Feb", "Mar", "Apr", "May"]
income = [5000, 6200, 5800, 7100, 6900]
expenses = [3200, 4100, 3900, 4500, 4300]

df = pd.DataFrame({
    "Month": months,
    "Income": income,
    "Expenses": expenses
})

st.subheader("Financial Data")
st.dataframe(df)

st.subheader("Income Chart")
st.line_chart(df.set_index("Month")["Income"])

st.subheader("Expense Chart")
st.bar_chart(df.set_index("Month")["Expenses"])

profit = np.sum(income) - np.sum(expenses)

st.metric("Total Profit", f"${profit}")
