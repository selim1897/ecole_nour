from PIL import Image
import numpy as np
import pytesseract 
from gtts import gTTS
from io import BytesIO
import streamlit as st
import pdf2image as pdf


st.set_page_config(page_title="Input", page_icon="🏠️", layout="centered", initial_sidebar_state="auto", menu_items=None)

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def check(txt_extracted):
    if txt_extracted is None or txt_extracted == "":
            if genre == "عربي":
                txt_extracted = "لا يوجد نص"
            elif genre == "Français":
                txt_extracted = "Il n'y a pas de texte"
            else:
                txt_extracted = "There is no text"
    return txt_extracted

genre = st.radio(
    "",
    ["عربي", "Français", "English"],
    horizontal=True,
)

if genre == "عربي":
    lg = "ara"
    lg_mp3 = "ar"
    confirm = "استمع"
elif genre == "Français":
    lg = "fra"
    lg_mp3 = "fr"
    confirm = "Ecoutez"
else:
    lg = "eng"
    lg_mp3 = "en"
    confirm = "Listen"


tab1, tab2 = st.tabs(["Text", "Document"])

with tab1:
    txt_extracted = st.text_area("text")
    if st.button(confirm):
        txt_extracted = check(txt_extracted)
        mp3_fp = BytesIO()
        tts = gTTS(txt_extracted, lang=lg_mp3)
        tts.write_to_fp(mp3_fp)
        st.audio(mp3_fp, format='audio/wav')


with tab2:    
    doc = st.file_uploader("Document", type=["pdf", "docx", "doc"], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="hidden")
    if st.button(confirm+" "):
        txt_extracted = ""
        if doc is not None:
            if doc.name.endswith('pdf'):
                images = pdf.convert_from_bytes(doc.getvalue())

                for im in images:
                    text = pytesseract.image_to_string(im, lang=lg)
                    txt_extracted += text + "\n"
        
        txt_extracted = check(txt_extracted)
        
        mp3_fp = BytesIO()
        tts = gTTS(txt_extracted, lang=lg_mp3)

        tts.write_to_fp(mp3_fp)

        st.audio(mp3_fp, format='audio/wav')
        st.write(txt_extracted)

