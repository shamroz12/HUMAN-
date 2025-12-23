
import numpy as np
AA = set("ACDEFGHIKLMNPQRSTVWY")

def clean_fasta(seq: str) -> str:
    seq = seq.upper().replace("\n","").replace(" ","")
    return "".join([a for a in seq if a in AA])

def sliding_windows(seq, k):
    return [(i+1, seq[i:i+k]) for i in range(0, len(seq)-k+1)]

def featurize(window, antigenicity, conservancy, length, class_flags, hpv_flags):
    return np.array([[
        antigenicity,
        conservancy,
        length,
        class_flags.get("CTL",0),
        class_flags.get("HTL",0),
        class_flags.get("B",0),
        hpv_flags.get("16",0),
        hpv_flags.get("18",0),
    ]])
