# save this as app.py
import streamlit as st
import matplotlib.pyplot as plt

st.title("Bar Plot from 3 Numbers")

# Input fields
num1 = st.number_input("Enter value for Group 1", value=0)
num2 = st.number_input("Enter value for Group 2", value=0)
num3 = st.number_input("Enter value for Group 3", value=0)

# Plot
if st.button("Generate Bar Plot"):
    fig, ax = plt.subplots()
    ax.bar(["Group 1", "Group 2", "Group 3"], [num1, num2, num3])
    st.pyplot(fig)