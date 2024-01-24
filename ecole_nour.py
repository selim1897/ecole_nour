from PIL import Image
import numpy as np
import pytesseract 
from gtts import gTTS
from io import BytesIO
import streamlit as st
import pdf2image as pdf


st.set_page_config(page_title="Input", page_icon="🏠️", layout="centered", initial_sidebar_state="auto", menu_items=None)

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

col = "text"

genre = st.radio(
    "",
    ["عربي", "Français", "English"],
    horizontal=True,
)

if genre == "عربي":
    lg = "ara"
    lg_mp3 = "ar"
elif genre == "Français":
    lg = "fra"
    lg_mp3 = "fr"
else:
    lg = "eng"
    lg_mp3 = "en"

def reset_doc():
    if txt_extracted is not None:
        del txt_extracted

def reset_text():
    if doc is not None:
        del doc

tab1, tab2 = st.tabs(["Text", "Pdf"])

with tab1:
    txt_extracted = st.text_area("text", on_change=reset_doc)

with tab2:    
    doc = st.file_uploader("", type=["pdf", "docx", "doc"], accept_multiple_files=False, key=None, help=None, on_change=reset_text, args=None, kwargs=None, disabled=False, label_visibility="hidden")

if doc is not None or txt_extracted is not None:
    if doc is not None:
        txt_extracted = ""
        if doc.name.endswith('pdf'):
            images = pdf.convert_from_bytes(doc.getvalue())

            for im in images:
                text = pytesseract.image_to_string(im, lang=lg)

                txt_extracted += text + "\n"
    
    if txt_extracted is None or txt_extracted == "":
        if genre == "عربي":
            txt_extracted = "لا يوجد نص"
        elif genre == "Français":
            txt_extracted = "Il n'y a pas de texte"
        else:
            txt_extracted = "There is no text"

    mp3_fp = BytesIO()
    tts = gTTS(txt_extracted, lang=lg_mp3)
    
    if doc is not None:
        tts.write_to_fp(mp3_fp)

    st.audio(mp3_fp, format='audio/wav')
    st.write(txt_extracted)

