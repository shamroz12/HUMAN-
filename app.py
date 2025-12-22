
import streamlit as st
import pickle
import numpy as np

# Load model and scaler
model = pickle.load(open("backend/rf_model.pkl", "rb"))
scaler = pickle.load(open("backend/scaler.pkl", "rb"))

st.title("HPV Epitope Scan (Fixed)")

seq = st.text_area("Paste peptide sequence (AA):")

if st.button("Predict"):
    if not seq:
        st.error("Enter a sequence.")
    else:
        length = len(seq)
        # dummy features for demo alignment
        features = np.array([[length, 1, 1, 1, 1, 1, 1, 1]])
        scaled = scaler.transform(features)
        pred = model.predict(scaled)[0]
        st.success(f"Prediction: {'Immunogenic' if pred==1 else 'Non-immunogenic'}")
