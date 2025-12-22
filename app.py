import streamlit as st
import pickle
import re
import numpy as np

# Load model & scaler
model = pickle.load(open("rf_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.title("🧬 HPV Epitope Scan")
st.write("Paste HPV protein sequence to scan for CTL / HTL / B-Cell epitopes.")

sequence = st.text_area("Enter amino acid sequence:", height=200)

# Parameters
st.sidebar.header("Filters & Parameters")

min_conservancy = st.sidebar.slider("Min Conservancy %", 0, 100, 70)
min_antigenicity = st.sidebar.slider("Min Antigenicity Score", 0.0, 1.0, 0.4)
min_length = st.sidebar.slider("Min Epitope Length", 8, 20, 9)

run = st.button("Scan Sequence")

def sliding_windows(seq, k):
    return [(seq[i:i+k], i, i+k) for i in range(len(seq)-k+1)]

def classify_epitope(ep):
    # Dummy placeholder features (extend later with real predictors)
    antigenicity = np.random.uniform(0,1)
    conservancy = np.random.uniform(0,100)
    length = len(ep)

    X = np.array([[antigenicity, conservancy, length]])
    X_scaled = scaler.transform(X)
    pred = model.predict(X_scaled)[0]

    return {
        "antigenicity": antigenicity,
        "conservancy": conservancy,
        "length": length,
        "prediction": "Immunogenic" if pred==1 else "Non-Immunogenic"
    }

if run:
    if not sequence:
        st.error("Enter a sequence first.")
    else:
        results = []
        for k in [9, 10, 15]:
            for ep, start, end in sliding_windows(sequence, k):
                res = classify_epitope(ep)
                if res["conservancy"] >= min_conservancy and \
                   res["antigenicity"] >= min_antigenicity and \
                   res["length"] >= min_length:
                    results.append((ep, start, end, res))

        if results:
            st.success(f"Detected {len(results)} potential epitopes.")
            st.dataframe([
                {
                    "Epitope": ep,
                    "Start": s,
                    "End": e,
                    **res
                } for ep, s, e, res in results
            ])
        else:
            st.warning("No epitopes passed your filters.")
