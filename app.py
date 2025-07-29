import streamlit as st
import numpy as np
import joblib
from PIL import Image

# Load the trained model
model = joblib.load("Farm_Irrigation_System.pkl")  

# App configuration
st.set_page_config(page_title="Smart Sprinkler System", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .header {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #2e86ab;
    }
    .sensor-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .prediction-box {
        background-color: #e9f5db;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
    }
    .on-status {
        color: #28a745;
        font-weight: bold;
    }
    .off-status {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Header section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<p class="header">Smart Sprinkler Irrigation System</p>', unsafe_allow_html=True)
    st.markdown("Enter scaled sensor values (0 to 1) to predict sprinkler status")
with col2:
    # You can add an image here if you have one
    # img = Image.open("irrigation.png")
    # st.image(img, width=100)

# Sensor input section
# 
 st.markdown("### 🌡️ Sensor Inputs")
with st.expander("Configure Sensor Values", expanded=True):
    cols = st.columns(4)  # 4 columns for better organization
    
    sensor_values = []
    for i in range(20):
        with cols[i % 4]:  # Distribute sliders across 4 columns
            val = st.slider(
                f"Sensor {i}",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.01,  
                key=f"sensor_{i}"
            )
            sensor_values.append(val)

# Prediction section
st.markdown("### 🔮 Prediction")
if st.button("Predict Sprinkler Status", use_container_width=True):
    input_array = np.array(sensor_values).reshape(1, -1)
    prediction = model.predict(input_array)[0]
    
    # Display results in a grid
    with st.container():
        st.success("Prediction completed successfully!")
        
        # Create a grid of 5x4 for the 20 sprinklers
        cols = st.columns(5)
        for i, status in enumerate(prediction):
            with cols[i % 5]:
                st.metric(
                    label=f"Parcel {i}",
                    value="ON" if status == 1 else "OFF",
                    delta="Watering" if status == 1 else "Idle",
                    delta_color="normal" if status == 0 else "inverse"
                )
        
        # Summary statistics
        on_count = sum(prediction)
        st.info(f"🌱 {on_count} sprinklers are ON | 🌵 {20 - on_count} sprinklers are OFF")
        
        # Visualization of active sprinklers
        st.markdown("#### Sprinkler Activation Map")
        grid_html = "<div style='display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;'>"
        for i, status in enumerate(prediction):
            color = "#4CAF50" if status == 1 else "#F44336"
            grid_html += f"""
                <div style='background-color: {color}; padding: 15px; border-radius: 5px; text-align: center; color: white;'>
                    Parcel {i}<br>{'ON' if status == 1 else 'OFF'}
                </div>
            """
        grid_html += "</div>"
        st.markdown(grid_html, unsafe_allow_html=True)