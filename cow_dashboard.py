import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

# Load model and data
model_path = os.path.join(current_directory, "stress_level_model.pkl")
    model = pickle.load(model_file)
cow_data = pd.read_excel(r"C:\Users\Admin\Desktop\streamlit ui\cow data accurate.xlsx")

# Function to fluctuate data with realistic changes
def fluctuate_data(row):
    row['Heart Rate'] += np.random.uniform(-1, 1)
    row['Body Temp'] += np.random.uniform(-0.05, 0.05)
    row['Activity Level'] += np.random.uniform(-0.5, 0.5) if row['Standing Time'] else np.random.uniform(-0.1, 0.1)
    row['Eating Behavior'] = 1 if np.random.rand() > 0.85 else 0
    row['Feeding Time'] += row['Eating Behavior']  # Per-minute gradual increase
    row['Vocalizations'] = np.random.randint(0, 3)  # Simplified logic
    if np.random.rand() > 0.5:
        row['Standing Time'] = 1 if np.random.rand() > 0.5 else 0
        row['Lying Time'] = 1 - row['Standing Time']
    return row

# Function to calculate weighted stress level
def calculate_weighted_stress(row):
    weights = {'Heart Rate': 0.3, 'Body Temp': 0.2, 'Activity Level': 0.1,
               'Eating Behavior': 0.1, 'Vocalizations': 0.2, 'Feeding Time': 0.1}
    heart_rate_norm = (row['Heart Rate'] - 50) / 60
    body_temp_norm = (row['Body Temp'] - 36) / 4
    activity_level_norm = row['Activity Level'] / 10  # Scaled down for realism
    eating_behavior_norm = row['Eating Behavior']
    vocalizations_norm = row['Vocalizations'] / 3
    feeding_time_norm = row['Feeding Time'] / 1440  # Adjusted for per-minute scale
    weighted_sum = (
        weights['Heart Rate'] * heart_rate_norm +
        weights['Body Temp'] * body_temp_norm +
        weights['Activity Level'] * activity_level_norm +
        weights['Eating Behavior'] * eating_behavior_norm +
        weights['Vocalizations'] * vocalizations_norm +
        weights['Feeding Time'] * feeding_time_norm
    )
    return 1 if weighted_sum > 0.55 else 0  # Increased threshold for more balance

# Streamlit configuration
st.set_page_config(page_title="Cow Metrics Dashboard", layout="wide")
st.title("Cow Metrics Dashboard")

# Update data for each cow and display in Streamlit
while True:
    cow_data = cow_data.apply(fluctuate_data, axis=1)  # Apply fluctuations
    cow_data['Predicted Stress Level'] = cow_data.apply(calculate_weighted_stress, axis=1)  # Calculate stress levels

    cols = st.columns(3)  # Arrange in 3 columns

    for i in range(len(cow_data)):
        cow = cow_data.iloc[i]
        col = cols[i % 3]  # Use modulo to wrap to new rows

        with col:
            st.markdown(
                f"""
                <div style="background-color: white; padding: 20px; border: 2px solid red; 
                            border-radius: 8px; width: 95%; color: black; margin-bottom: 15px;">
                    <h4 style="margin: 0; text-align: center;">Cow ID: {cow['Cow ID']}</h4>
                    <p><strong>Heart Rate:</strong> {int(cow['Heart Rate'])} bpm</p>
                    <p><strong>Body Temp:</strong> {cow['Body Temp']:.1f} °C</p>
                    <p><strong>Activity Level:</strong> {cow['Activity Level']:.2f}</p>
                    <p><strong>Eating Behavior:</strong> {int(cow['Eating Behavior'])}</p>
                    <p><strong>Vocalizations:</strong> {int(cow['Vocalizations'])}</p>
                    <p><strong>Feeding Time:</strong> {int(cow['Feeding Time'])}</p>
                    <p><strong>Standing Time:</strong> {int(cow['Standing Time'])}</p>
                    <p><strong>Lying Time:</strong> {int(cow['Lying Time'])}</p>
                    <p><strong>Stress Level:</strong> {"Stressed" if cow['Predicted Stress Level'] == 1 else "Not Stressed"}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    time.sleep(5)
    st.experimental_rerun()
