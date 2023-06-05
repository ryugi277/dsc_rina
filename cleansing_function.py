"""
Function untuk membersihkan data text
"""
import re

def text_cleansing(text):
    #bersihkan tanda baca (selain huruf dan angka)
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    #yang lain
    clean_text = clean_text.lower()
    return clean_text