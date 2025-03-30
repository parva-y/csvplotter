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
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    
    if categorical_columns:
        filter_col = st.selectbox("Select a column to filter", categorical_columns)
        filter_values = df[filter_col].unique()
        selected_values = st.multiselect("Select values to filter", filter_values, default=filter_values)
        df = df[df[filter_col].isin(selected_values)]
    
    if numeric_columns:
        x_axis = st.selectbox("Select X-axis", numeric_columns)
        y_axis = st.selectbox("Select Y-axis", numeric_columns)
        
        calc_expression = st.text_area("Enter a calculation (e.g., df['column1'] + df['column2'])")
        
        if calc_expression:
            try:
                df['Calculated'] = eval(calc_expression, {"df": df, "pd": pd})
                st.write("Calculated Values:")
                st.write(df[['Calculated']].head())
            except Exception as e:
                st.write(f"Error in calculation: {e}")
        
        fig, ax = plt.subplots()
        ax.scatter(df[x_axis], df[y_axis], alpha=0.7)
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"Scatter Plot of {y_axis} vs {x_axis}")
        st.pyplot(fig)
    else:
        st.write("No numeric columns found in the uploaded CSV.")
