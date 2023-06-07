""" 
Function untuk membersihkan data text
"""
import re
import pandas as pd


#load data
alay = pd.read_csv("csv_data/alay.csv", encoding="latin-1", names=("original","replacement"))
abusive = pd.read_csv("csv_data/abusive.csv", encoding="latin-1") 



# cleaning preprocessing
# aturan 1: hapus karakter yg tidak diperlukan
def delete_irr_char(text):
    text = re.sub('\n',' ',text) # Hapus baris baru '\n'
    text = re.sub('rt',' ',text) # Hapus simbol retweet
    text = re.sub('user',' ',text) # Hapus username
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # Hapus URL
    text = re.sub('  +', ' ', text) # Hapus spasi berlebih
    text = re.sub(r'pic.twitter.com.[\w]+', '', text) # Hapus gambar 
    text = re.sub('gue','saya',text) # Ganti gue ke saya
    return text

# aturan 2: bersihkan tanda baca 
def text_cleansing(text):
    # Bersihkan tanda baca (selain huruf dan angka)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower()
    return text

# aturan 3: ubah kata alay ke kata baku
alay_dict_map = dict(zip(alay['original'], alay['replacement']))
def normalize_alay(text):
    return ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])

# aturan 4: hapus kata kasar
def remove_abusive(text):
    text = ' '.join(['' if word in abusive.values else word for word in text.split(' ')])
    text = re.sub('  +', ' *** ', text) # Hapus spasi extra 
    text = text.strip()
    return text
    
# penggabungan semua aturan
def preprocessing(text):
    text = delete_irr_char(text) # 1
    text = text_cleansing(text) # 2
    text = normalize_alay(text) # 3
    text = remove_abusive(text) # 4
   
    
    return text


def cleansing_files(file_upload):
    # Read csv file upload, jika error dengan metode biasa, gunakan encoding latin-1
    try:
        df_upload = pd.read_csv(file_upload)
    except:
        df_upload = pd.read_csv(file_upload, encoding="latin-1")
    print("Read dataframe from Upload success!")
    # Ambil hanya kolom pertama saja 
    df_upload = pd.DataFrame(df_upload.iloc[:,0])
    # Rename kolom menjadi "raw_text"
    df_upload.columns = ["raw_text"]
    # Bersihkan text menggunakan fungsi text_cleansing
    
    # Simpan di kolom "clean_text"
    df_upload["clean_text"] = df_upload["raw_text"].apply(preprocessing)
    print("Cleansing text success!")
    return df_upload
    