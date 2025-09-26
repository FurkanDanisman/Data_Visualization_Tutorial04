import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# File path for storing data
DATA_FILE = "Data_vis_tutorial04.csv"

# Initialize the CSV file with headers if it doesn't exist
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Name", "Group1", "Group2", "Group3"])
    df_init.to_csv(DATA_FILE, index=False)

# Load existing data
df = pd.read_csv(DATA_FILE)

st.title("Collaborative Bar Plot App")

# Input form
name = st.text_input("Enter your name")
group1 = st.number_input("Enter value for Group 1", value=0)
group2 = st.number_input("Enter value for Group 2", value=0)
group3 = st.number_input("Enter value for Group 3", value=0)

# Check if name already exists
if name and name not in df["Name"].values:
    if st.button("Submit"):
        new_entry = pd.DataFrame([[name, group1, group2, group3]], columns=["Name", "Group1", "Group2", "Group3"])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Your input has been recorded.")
else:
    if name:
        st.info("You have already submitted your input. Showing current average plot.")

# Calculate averages
if not df.empty:
    avg_group1 = df["Group1"].mean()
    avg_group2 = df["Group2"].mean()
    avg_group3 = df["Group3"].mean()

    # Plotting
    fig, ax = plt.subplots()
    ax.bar(["Group 1", "Group 2", "Group 3"], [avg_group1, avg_group2, avg_group3], color=["blue", "green", "orange"])
    ax.set_ylabel("Average Value")
    ax.set_title("Average Values from All Submissions")
    st.pyplot(fig)
else:
    st.warning("No data available yet.")
