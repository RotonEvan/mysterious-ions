import streamlit as st
import numpy as np
import func as obj

st.title("Mysterion")
st.sidebar.title("Mysterion")

st.markdown("Mysterion Block Cipher Encrypt-Decrypt Tool")
st.sidebar.markdown("Mysterion Block Cipher Encrypt-Decrypt Tool")

pt = "01010000B2C3D4E5F60718293A4B5C6D"
key = "0205060752F3E1F2132435465B6C7D88"

pt = st.sidebar.text_input("Plaintext in hexadecimal", pt)
key = st.sidebar.text_input("Key in hexadecimal", key)



def encrypt(m, k):
    m = list(bytearray.fromhex(m))
    k = list(bytearray.fromhex(k))

    # spliting message in blocks 
    m = np.array([m[i*4:(i+1)*4] for i in range(4)])
    k = np.array([k[i*4:(i+1)*4] for i in range(4)])

    ct = obj.Mysterion128(k, m)
    cpt = obj.InvMysterion128(ct, k)

    h_ct = ""
    for i in ct:
        h_ct += ''.join('{:02x}'.format(x) for x in i)
    
    h_cpt = ""
    for i in cpt:
        h_cpt += ''.join('{:02x}'.format(x) for x in i)

    return (h_ct, h_cpt)

ct, cpt = encrypt(pt, key)

st.text("Encryption")
st.text("Plaintext : " + pt)
st.text("Ciphertext : " + ct)

st.text("Decryption")
st.text("Ciphertext : " + ct)
st.text("Computed Plaintext : " + cpt)