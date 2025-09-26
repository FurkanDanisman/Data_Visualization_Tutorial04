import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Set matplotlib style for better aesthetics
plt.style.use('seaborn-v0_8-whitegrid')

# File path for storing data
DATA_FILE = "Data_vis_tutorial04.csv"

# Initialize the CSV file with headers if it doesn't exist
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Name", "Visualization design", "Write-up", "Other"])
    df_init.to_csv(DATA_FILE, index=False)

# Load existing data
df = pd.read_csv(DATA_FILE)

st.title("🎨 Collaborative Bar Plot App")
st.markdown("---")

# Input form with improved layout
col1, col2 = st.columns([2, 1])

with col1:
    name = st.text_input("👤 Enter your name", placeholder="Your name here...")
    
    st.markdown("### 📊 Enter your values:")
    
    # Input fields with constraints
    viz_design = st.number_input(
        "🎯 Visualization design (0-4)", 
        min_value=0, max_value=4, value=0,
        help="Rate from 0 to 4"
    )
    
    writeup = st.number_input(
        "📝 Write-up (0-4)", 
        min_value=0, max_value=4, value=0,
        help="Rate from 0 to 4"
    )
    
    other = st.number_input(
        "🔧 Other (0-1)", 
        min_value=0, max_value=1, value=0,
        help="Rate from 0 to 1"
    )

with col2:
    st.markdown("### 📋 Current Stats")
    if not df.empty:
        st.metric("Total Submissions", len(df))
        st.metric("Avg Viz Design", f"{df['Visualization design'].mean():.2f}")
        st.metric("Avg Write-up", f"{df['Write-up'].mean():.2f}")
        st.metric("Avg Other", f"{df['Other'].mean():.2f}")

# Check if name already exists
if name and name not in df["Name"].values:
    if st.button("✅ Submit", type="primary"):
        new_entry = pd.DataFrame([[name, viz_design, writeup, other]], 
                               columns=["Name", "Visualization design", "Write-up", "Other"])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("🎉 Your input has been recorded!")
        st.balloons()
else:
    if name:
        st.info("ℹ️ You have already submitted your input. Showing current average plot.")

st.markdown("---")

# Calculate averages and create beautiful plot
if not df.empty:
    avg_viz = df["Visualization design"].mean()
    avg_writeup = df["Write-up"].mean() 
    avg_other = df["Other"].mean()
    
    # Create a beautiful plot with larger size for better readability
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Define categories and values
    categories = ["Visualization design", "Write-up", "Other"]
    values = [avg_viz, avg_writeup, avg_other]
    max_values = [4, 4, 1]  # Maximum possible values for each category
    
    # Create beautiful gradient colors
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # Create bars with enhanced styling
    bars = ax.bar(categories, values, color=colors, alpha=0.8, 
                  edgecolor='white', linewidth=3)
    
    # Add value labels on top of bars with much larger font
    for i, (bar, value) in enumerate(zip(bars, values)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{value:.2f}', ha='center', va='bottom', 
                fontsize=24, fontweight='bold', color='#2C3E50')
    
    # Add individual data points as scatter plot overlay
    for i, category in enumerate(categories):
        category_data = df[category].values
        x_positions = np.full(len(category_data), i)
        # Add some jitter for better visibility
        x_jitter = x_positions + np.random.normal(0, 0.1, len(category_data))
        
        ax.scatter(x_jitter, category_data, alpha=0.6, s=80, 
                  color='#34495E', edgecolors='white', linewidth=2,
                  zorder=3)
    
    # Customize the plot appearance with MUCH larger fonts
    ax.set_ylabel('Average Score', fontsize=28, fontweight='bold', color='#2C3E50')
    ax.set_title('📊 Average Scores from All Submissions', 
                fontsize=36, fontweight='bold', color='#2C3E50', pad=30)
    
    # Set y-axis to show only integer values from 0 to 4
    ax.set_ylim(0, 4.5)
    
    # Add horizontal grid lines
    ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=1)
    ax.set_axisbelow(True)
    
    # Customize tick labels with much larger fonts
    ax.tick_params(axis='x', labelsize=22, colors='#2C3E50')
    ax.tick_params(axis='y', labelsize=22, colors='#2C3E50')
    
    # Set y-axis ticks to only show integers 0, 1, 2, 3, 4
    ax.set_yticks([0, 1, 2, 3, 4])
    
    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_color('#BDC3C7')
    ax.spines['bottom'].set_linewidth(2)
    
    # Set background color
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#FAFAFA')
    
    # Adjust layout
    plt.tight_layout()
    
    # Display the plot
    st.pyplot(fig)
    
    # Add some additional information
    st.markdown("### 📈 Data Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        **Visualization Design**
        - Average: {avg_viz:.2f}/4
        - Range: 0-4
        - Submissions: {len(df[df['Visualization design'] > 0])}
        """)
    
    with col2:
        st.markdown(f"""
        **Write-up**
        - Average: {avg_writeup:.2f}/4
        - Range: 0-4
        - Submissions: {len(df[df['Write-up'] > 0])}
        """)
    
    with col3:
        st.markdown(f"""
        **Other**
        - Average: {avg_other:.2f}/1
        - Range: 0-1
        - Submissions: {len(df[df['Other'] > 0])}
        """)

else:
    st.warning("⚠️ No data available yet. Be the first to submit!")
    # Show empty plot with proper styling and large fonts
    fig, ax = plt.subplots(figsize=(16, 10))
    categories = ["Visualization design", "Write-up", "Other"]
    ax.bar(categories, [0, 0, 0], color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.3)
    ax.set_ylabel('Average Score', fontsize=28, fontweight='bold')
    ax.set_title('📊 Average Scores from All Submissions', fontsize=36, fontweight='bold', pad=30)
    ax.set_ylim(0, 4.5)
    ax.grid(True, axis='y', alpha=0.3)
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.tick_params(axis='x', labelsize=22, colors='#2C3E50')
    ax.tick_params(axis='y', labelsize=22, colors='#2C3E50')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    st.pyplot(fig)
