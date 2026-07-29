import pandas as pd
from pythermalcomfort.models import pet_steady

# Membaca file Excel
df = pd.read_excel("Data_TULT3B_PET.xlsx")

# Fungsi konversi Va
def convert_va(x):

    # Jika data berupa waktu Excel
    if pd.notnull(x):

        try:
            jam = x.hour
            menit = x.minute

            return float(f"{jam}.{menit:02d}")

        except:
            return None

    return None

# Konversi Va
df["Va_fix"] = df["Va"].apply(convert_va)

# Konversi kolom lain
df["Ta"] = pd.to_numeric(df["Ta"], errors="coerce")
df["Tmrt"] = pd.to_numeric(df["Tmrt"], errors="coerce")
df["RH"] = pd.to_numeric(df["RH"], errors="coerce")

# Hapus data kosong
df = df.dropna(subset=["Va_fix", "Ta", "Tmrt", "RH"])

# Hitung PET
hasil_pet = []

for i in range(len(df)):

    hasil = pet_steady(
        tdb=df["Ta"].iloc[i],
        tr=df["Tmrt"].iloc[i],
        v=df["Va_fix"].iloc[i],
        rh=df["RH"].iloc[i],

        met=1.2,
        clo=0.5,

        age=21,
        sex="male",
        weight=58.8,
        height=1.651
    )

    hasil_pet.append(hasil.pet)

# Simpan hasil
df["PET"] = hasil_pet

df.to_excel("hasil_pet_TULT3B.xlsx", index=False)

print("Perhitungan PET selesai")