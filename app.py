import streamlit as st
import pandas as pd
import numpy as np
import pickle

# import the model
pipe = pickle.load(open("pipe.pkl", "rb"))
df = pd.read_pickle(open("df.pkl", "rb"))

st.title("Laptop Price Predictor")

# brand
company = st.selectbox('Brand', df['Company'].unique())

# type of laptop
type = st.selectbox('Type', df['TypeName'].unique())

# ram
ram = st.selectbox('Ram (GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])

# weight
weight = st.number_input('Weight of laptop (Kg)', value=2.20)

# touchscreen
touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])

# IPS
ips = st.selectbox('IPS', ['No', 'Yes'])

# screen size
screen_size = st.number_input('Screen size (Inches)', value=15.6)

# resolution
resolution = st.selectbox('Screen Resolution', [
                          '1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440'])

# cpu
cpu = st.selectbox('CPU', df['Cpu brand'].unique())

# HDD
hdd = st.selectbox('HDD (GB)', [0, 128, 256, 512, 1024, 2048])

# SSD
ssd = st.selectbox('SSD (GB)', [0, 8, 128, 256, 512, 1024])

# gpu
gpu = st.selectbox('GPU', df['Gpu brand'].unique())

# OS
os = st.selectbox('OS', df['os'].unique())

if st.button('Predict Price'):
    # query
    x_res = int(resolution.split('x')[0])
    y_res = int(resolution.split('x')[1])
    ppi = (x_res**2 + y_res**2)**0.5 / screen_size
    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0

    query = np.array([company, type, ram, weight, touchscreen,
                     ips, ppi, cpu, hdd, ssd, gpu, os], dtype=object)

    query = query.reshape(1, 12)
    pred_price = np.exp(pipe.predict(query)[0])
    st.title(f'Predicted price is: Rs. {pred_price:.2f}')
