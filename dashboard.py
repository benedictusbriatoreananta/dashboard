import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Judul Aplikasi
st.title("Aplikasi Peta dengan Data Excel")

# Langkah 3: Unggah File Excel
uploaded_files = st.file_uploader("Unggah file Excel", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    all_dfs = {}
    for uploaded_file in uploaded_files:
        # Baca semua sheet dari file Excel
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names

        # Pilih sheet
        sheet = st.selectbox(f"Pilih sheet untuk {uploaded_file.name}", sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=sheet)
        all_dfs[uploaded_file.name] = df

    # Gabungkan semua dataframe dari semua file
    combined_df = pd.concat(all_dfs.values(), ignore_index=True)

    # Tampilkan dataframe gabungan
    st.write("Data dari semua file yang diunggah:")
    st.dataframe(combined_df)

    # Pilih kolom untuk operator
    operator_col = st.selectbox("Pilih kolom operator", combined_df.columns)
    unique_operators = combined_df[operator_col].unique()
    operators = st.multiselect("Pilih operator", unique_operators)

    # Filter data berdasarkan operator
    df_filtered = combined_df[combined_df[operator_col].isin(operators)]

    # Pilih kolom untuk latitude dan longitude
    lat_col = st.selectbox("Pilih kolom latitude", combined_df.columns)
    lon_col = st.selectbox("Pilih kolom longitude", combined_df.columns)

    # Pilih kolom data untuk dibandingkan
    data_columns = st.multiselect("Pilih kolom data untuk dibandingkan", combined_df.columns)

    # Warna khusus untuk setiap operator
    operator_colors = {
        'Telkomsel': 'red',
        'Smartfren': 'blue',
        'Indosat': 'green',
        'XL': 'purple'
    }

    # Pastikan kolom latitude dan longitude dipilih
    if lat_col and lon_col and not df_filtered.empty:
        # Langkah 4: Buat Peta Folium
        m = folium.Map(location=[df_filtered[lat_col].mean(), df_filtered[lon_col].mean()], zoom_start=12)

        # Tambahkan titik-titik ke peta dengan popup untuk data yang dipilih
        for i, row in df_filtered.iterrows():
            popup_text = "<br>".join([f"{col}: {row[col]}" for col in data_columns])
            operator = row[operator_col]
            color = operator_colors.get(operator, 'gray')  # Default color is gray if operator is not in the dictionary
            folium.Marker(
                location=[row[lat_col], row[lon_col]],
                popup=popup_text,
                icon=folium.Icon(color=color)
            ).add_to(m)

        # Tampilkan peta
        st_folium(m, width=700, height=500)
    else:
        st.write("Pilih setidaknya satu operator untuk menampilkan data.")
