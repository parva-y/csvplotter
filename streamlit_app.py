import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.title("Cohort Data Trend Visualizer")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=['date'])
    st.write("Data Preview:")
    st.write(df.head())
    
    # Ensure necessary columns exist
    required_columns = {'date', 'data_set', 'audience_size', 'app_opens', 'atc', 'transactors', 'orders', 'gmv', 'cohort'}
    if not required_columns.issubset(df.columns):
        st.write("Missing required columns in the CSV file.")
    else:
        # Calculate metrics
        df['gmv_per_audience'] = df['gmv'] / df['audience_size']
        df['app_opens_per_audience'] = df['app_opens'] / df['audience_size']
        df['orders_per_audience'] = df['orders'] / df['audience_size']
        df['transactors_per_audience'] = df['transactors'] / df['audience_size']
        
        # Select cohort
        cohort_options = df['cohort'].unique()
        selected_cohort = st.selectbox("Select Cohort", cohort_options)
        df_filtered = df[df['cohort'] == selected_cohort]
        
        # Select metric to plot
        metric_options = ['gmv_per_audience', 'app_opens_per_audience', 'orders_per_audience', 'transactors_per_audience']
        selected_metric = st.selectbox("Select Metric", metric_options)
        
        # Select campaign dates
        campaign_dates = st.multiselect("Select Campaign Dates", df_filtered['date'].dt.date.unique())
        
        # Plot trend for both data sets
        fig, ax = plt.subplots(figsize=(19.2, 10.8))
        for data_set in df_filtered['data_set'].unique():
            df_subset = df_filtered[df_filtered['data_set'] == data_set].sort_values(by='date')
            ax.plot(df_subset['date'], df_subset[selected_metric], label=data_set, marker='o')
        
        # Mark campaign dates
        for campaign_date in campaign_dates:
            ax.axvline(pd.to_datetime(campaign_date), color='red', linestyle='--', alpha=0.7, label='Campaign Day' if campaign_date == campaign_dates[0] else "")
        
        # Format x-axis to show only day and month
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        
        ax.set_xlabel("Date")
        ax.set_ylabel(selected_metric.replace("_", " ").title())
        ax.set_title(f"{selected_metric.replace('_', ' ').title()} Trend for Cohort {selected_cohort}")
        ax.legend()
        ax.grid()
        st.pyplot(fig)
