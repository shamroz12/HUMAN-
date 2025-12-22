
import streamlit as st
import pickle
import numpy as np

model = pickle.load(open("backend/rf_model.pkl", "rb"))
scaler = pickle.load(open("backend/scaler.pkl", "rb"))

st.title("HPV Epitope Scan")
st.write("Demo app placeholder. Full features pending.")
