import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("CSV Data Visualizer")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(df.head())
    
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_columns:
        x_axis = st.selectbox("Select X-axis", numeric_columns)
        y_axis = st.selectbox("Select Y-axis", numeric_columns)
        
        calc_option = st.selectbox("Choose a calculated parameter", ["None", "Mean", "Sum", "Standard Deviation"])
        
        if calc_option != "None":
            if calc_option == "Mean":
                st.write(f"Mean of {y_axis}: {df[y_axis].mean()}")
            elif calc_option == "Sum":
                st.write(f"Sum of {y_axis}: {df[y_axis].sum()}")
            elif calc_option == "Standard Deviation":
                st.write(f"Standard Deviation of {y_axis}: {df[y_axis].std()}")
        
        fig, ax = plt.subplots()
        ax.scatter(df[x_axis], df[y_axis], alpha=0.7)
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"Scatter Plot of {y_axis} vs {x_axis}")
        st.pyplot(fig)
    else:
        st.write("No numeric columns found in the uploaded CSV.")
