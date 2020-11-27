import streamlit as st
import numpy as np
import func as obj

st.title("Mysterion")
st.sidebar.title("Mysterion")

st.markdown("Mysterion Block Cipher Encrypt-Decrypt Tool")
st.sidebar.markdown("Mysterion Block Cipher Encrypt-Decrypt Tool")

inpt = "01010000B2C3D4E5F60718293A4B5C6D"
key = "0205060752F3E1F2132435465B6C7D88"

inpt = st.sidebar.text_input("Plaintext in hexadecimal", inpt)
key = st.sidebar.text_input("Key in hexadecimal", key)

NR = st.sidebar.slider("Rounds", 1, 16, 12, 1)

opt = st.sidebar.radio('Operation', ('Encrypt', 'Decrypt', 'Both'))

def encrypt(m, k):
    m = list(bytearray.fromhex(m))
    k = list(bytearray.fromhex(k))

    # spliting message in blocks 
    m = np.array([m[i*4:(i+1)*4] for i in range(4)])
    k = np.array([k[i*4:(i+1)*4] for i in range(4)])

    ct = obj.Mysterion128(k, m, NR)
    
    h_ct = ""
    for i in ct:
        h_ct += ''.join('{:02x}'.format(x) for x in i)

    return h_ct

def decrypt(m, k):
    m = list(bytearray.fromhex(m))
    k = list(bytearray.fromhex(k))

    # spliting message in blocks 
    m = np.array([m[i*4:(i+1)*4] for i in range(4)])
    k = np.array([k[i*4:(i+1)*4] for i in range(4)])

    cpt = obj.InvMysterion128(m, k, NR)

    h_cpt = ""
    for i in cpt:
        h_cpt += ''.join('{:02x}'.format(x) for x in i)
    
    return h_cpt

def endecrypt(m, k):
    m = list(bytearray.fromhex(m))
    k = list(bytearray.fromhex(k))

    # spliting message in blocks 
    m = np.array([m[i*4:(i+1)*4] for i in range(4)])
    k = np.array([k[i*4:(i+1)*4] for i in range(4)])

    ct = obj.Mysterion128(k, m, NR)
    cpt = obj.InvMysterion128(ct, k, NR)
    
    h_ct = ""
    for i in ct:
        h_ct += ''.join('{:02x}'.format(x) for x in i)
    
    h_cpt = ""
    for i in cpt:
        h_cpt += ''.join('{:02x}'.format(x) for x in i)
    
    return (h_ct, h_cpt)

if opt == "Encrypt":
    ct = encrypt(inpt, key)
    st.text("Encryption")
    st.text("Plaintext : " + inpt)
    st.text("Ciphertext : " + ct)
elif opt == "Decrypt":
    cpt = decrypt(inpt, key)
    st.text("Decryption")
    st.text("Ciphertext : " + inpt)
    st.text("Computed Plaintext : " + cpt)
else:
    ct, cpt = endecrypt(inpt, key)
    st.text("Encryption")
    st.text("Plaintext : " + inpt)
    st.text("Ciphertext : " + ct)
    st.text("Decryption")
    st.text("Ciphertext : " + ct)
    st.text("Computed Plaintext : " + cpt)