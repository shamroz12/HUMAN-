import streamlit as st
import numpy as np
import pickle
from utils import clean_fasta, sliding_windows, featurize
st.set_page_config(page_title="HPV Epitope Mapper", layout="wide")

model = pickle.load(open("rf_model.pkl","rb"))
scaler = pickle.load(open("scaler.pkl","rb"))

st.title("HPV Advanced Epitope Mapping Tool")
st.caption("ML-assisted epitope prioritization (CTL/HTL/B)")

seq = st.text_area("Paste protein sequence (FASTA or raw)", height=180)

min_len = st.slider("Min Length", 8, 15, 9)
max_len = st.slider("Max Length", 9, 30, 15)
antigenicity = st.slider("Antigenicity (proxy)", 0.0, 1.5, 0.6, 0.01)
conservancy = st.slider("Conservancy (%)", 0, 100, 80)

c1, c2, c3 = st.columns(3)
class_CTL = c1.checkbox("CTL")
class_HTL = c2.checkbox("HTL")
class_B   = c3.checkbox("B-cell")

h1, h2 = st.columns(2)
hpv16 = h1.checkbox("HPV-16")
hpv18 = h2.checkbox("HPV-18")

if st.button("Map Epitopes"):
    clean = clean_fasta(seq)
    if len(clean) < min_len:
        st.error("Sequence too short after cleaning.")
    else:
        class_flags = {"CTL": int(class_CTL), "HTL": int(class_HTL), "B": int(class_B)}
        hpv_flags = {"16": int(hpv16), "18": int(hpv18)}
        rows = []
        for k in range(min_len, max_len+1):
            for start, pep in sliding_windows(clean, k):
                X = featurize(pep, antigenicity, conservancy, k, class_flags, hpv_flags)
                Xs = scaler.transform(X)
                prob = model.predict_proba(Xs)[0][1]
                rows.append({"start": start, "end": start+k-1, "length": k, "peptide": pep, "score": round(float(prob),4)})
        import pandas as pd
        df = pd.DataFrame(rows).sort_values("score", ascending=False)
        st.dataframe(df.head(100), use_container_width=True)

