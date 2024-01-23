from PIL import Image
import numpy as np
import pytesseract 
from gtts import gTTS
from io import BytesIO
import streamlit as st
import pdf2image as pdf


st.set_page_config(page_title="Input", page_icon="🏠️", layout="centered", initial_sidebar_state="auto", menu_items=None)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

label = ""

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

#img_file_buffer = st.camera_input(label)
    
doc = st.file_uploader("", type=["pdf", "docx", "doc"], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="hidden")

if doc is not None:
    # To read image file buffer as a PIL Image:
    #img = Image.open(img_file_buffer)
    #text_from_img = pytesseract.image_to_string(img, lang=lg)
    text_from_img = ""
    if doc.name.endswith('pdf'):
        images = pdf.convert_from_bytes(doc.getvalue())

    for im in images:
        text = pytesseract.image_to_string(im, lang=lg)

        text_from_img += text + "\n"
    
    
    
    if text_from_img is None or text_from_img == "":
        if genre == "عربي":
            text_from_img = "لا يوجد نص في الصورة"
        elif genre == "Français":
            text_from_img = "Il n'y a pas de texte dans l\'image"
        else:
            text_from_img = "There is no text in the image"

    mp3_fp = BytesIO()
    tts = gTTS(text_from_img, lang=lg_mp3)
    tts.write_to_fp(mp3_fp)

    st.audio(mp3_fp, format='audio/wav')

