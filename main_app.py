import os
import streamlit as st
import pandas as pd
import plotly.express as px
from manajer_kas import KasManager
from model import Pemasukan, Pengeluaran
from konfigurasi import KATEGORI_MASUK, KATEGORI_KELUAR

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Kas Racana Pandawa", page_icon="⚜️", layout="wide", initial_sidebar_state="expanded")

# 2. Injeksi CSS Premium (Penyempurnaan Teks Sidebar & Layout Logo)
st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #3E2723;
    }
    
    /* Menyempurnakan Tampilan Logo agar nyatu (App Icon Style) */
    [data-testid="stSidebar"] img {
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    /* Trik Tombol Menu Sidebar (TULISAN DIJAMIN TERANG) */
    [data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child { display: none !important; }
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        width: 100%; padding: 15px 20px; margin-bottom: 12px; border-radius: 10px;
        background-color: transparent; transition: all 0.3s ease; cursor: pointer; border: 1px solid transparent;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: rgba(200, 159, 112, 0.2); transform: translateX(5px);
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background-color: #C89F70 !important; border-left: 6px solid #FFFFFF; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    /* PERBAIKAN WARNA TEKS MENU */
    [data-testid="stSidebar"] div[role="radiogroup"] label p { 
        font-weight: 700 !important; 
        font-size: 18px !important; 
        color: #FDFBF7 !important; /* Ini yang bikin tulisannya jadi putih/krem! */
        margin: 0 !important; 
    }

    /* Kotak Khusus AI Insight */
    .insight-panel {
        background: linear-gradient(145deg, #FFFFFF, #F8F5F0);
        padding: 25px 30px; 
        border-radius: 16px; 
        margin-bottom: 30px;
        border-left: 8px solid #C89F70;
        box-shadow: 0 10px 30px rgba(62, 39, 35, 0.08);
    }
    
    .data-card {
        background: #FFFFFF; padding: 24px; border-radius: 12px; margin-bottom: 20px;
        border: 1px solid #EFEBE1; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }

    button[kind="primary"] {
        background-color: #C89F70 !important; border: none !important; color: white !important;
        font-weight: 700 !important; font-size: 18px !important; padding: 10px 20px !important; border-radius: 8px !important;
    }
    button[kind="primary"]:hover { background-color: #B0885A !important; }
    div[data-testid="stForm"], .css-1d391kg { background-color: #FFFFFF; border-radius: 12px; border: 1px solid #EFEBE1; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }
    </style>
    """, unsafe_allow_html=True)

# 3. Inisialisasi Logika Bisnis
@st.cache_resource
def get_manager():
    return KasManager()

manager = get_manager()

def format_rp(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

# ==========================================
# --- SIDEBAR NAVIGATION ---
# ==========================================
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    # Komposisi kolom logo diperbaiki biar proporsional dan tidak terlalu besar
    if os.path.exists("logo_racana.png"):
        col1, col2, col3 = st.columns([1, 1.3, 1])
        with col2:
            st.image("logo_racana.png", use_container_width=True)
        st.markdown("<h2 style='text-align: center; color: #D4A373; margin-top: 15px; margin-bottom: 30px; font-size: 24px; font-weight: 800;'>Racana<br>Pandawa</h2>", unsafe_allow_html=True)
    elif os.path.exists("logo_racana.jpg"):
        col1, col2, col3 = st.columns([1, 1.3, 1])
        with col2:
            st.image("logo_racana.jpg", use_container_width=True)
        st.markdown("<h2 style='text-align: center; color: #D4A373; margin-top: 15px; margin-bottom: 30px; font-size: 24px; font-weight: 800;'>Racana<br>Pandawa</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #D4A373; margin-bottom: 30px; font-size: 32px;'>⚜️ Racana<br>Pandawa</h1>", unsafe_allow_html=True)
    
    menu_pilihan = st.radio("MAIN MENU", ["📊 Dashboard", "📝 Input Transaksi", "🔍 Audit & Riwayat"], label_visibility="collapsed")
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A67C52; font-size: 12px;'>Sistem Pengelolaan Kas v2.0</p>", unsafe_allow_html=True)

t_masuk, t_keluar, saldo, df = manager.get_ringkasan()

# ==========================================
# --- MENU 1: DASHBOARD ---
# ==========================================
if menu_pilihan == "📊 Dashboard":
    st.markdown("<h1 style='color: #3E2723; font-weight: 800; margin-bottom: 25px;'>Dashboard Keuangan</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="display: flex; gap: 20px; margin-bottom: 30px; width: 100%;">
       <div style="flex: 1.6; background: linear-gradient(135deg, #6D4C41, #A67C52); padding: 35px 40px; border-radius: 16px; color: white; box-shadow: 0 8px 20px rgba(74, 54, 35, 0.2);">
           <p style="margin:0; font-size: 18px; color: #E8D8C8; font-weight: 600;">Total Saldo Aktif 👁️</p>
           <h1 style="margin:15px 0 25px 0; font-size: 48px; color: white; font-weight: 800;">{format_rp(saldo)}</h1>
           <p style="margin:0; font-size: 16px; color: #E8D8C8;">Dana Siap Digunakan</p>
       </div>
       <div style="flex: 1; background: #FFFFFF; padding: 30px; border-radius: 16px; border: 1px solid #EFEBE1; box-shadow: 0 4px 12px rgba(0,0,0,0.03); display: flex; flex-direction: column; justify-content: center;">
           <p style="margin:0; font-size: 16px; color: #5C4033; font-weight: 700;">Total Pemasukan 📥</p>
           <h2 style="margin:15px 0 0 0; font-size: 32px; color: #1A1A1A; font-weight: 800;">{format_rp(t_masuk)}</h2>
       </div>
       <div style="flex: 1; background: #FFFFFF; padding: 30px; border-radius: 16px; border: 1px solid #EFEBE1; box-shadow: 0 4px 12px rgba(0,0,0,0.03); display: flex; flex-direction: column; justify-content: center;">
           <p style="margin:0; font-size: 16px; color: #5C4033; font-weight: 700;">Total Pengeluaran 📤</p>
           <h2 style="margin:15px 0 0 0; font-size: 32px; color: #1A1A1A; font-weight: 800;">{format_rp(t_keluar)}</h2>
       </div>
    </div>
    """, unsafe_allow_html=True)

    # KOTAK KHUSUS AI INSIGHT DENGAN FULL HTML (BEBAS BUG)
    html_insight = """
    <div class='insight-panel'>
        <h3 style='color: #3E2723; margin-top: 0; margin-bottom: 15px;'>💡 Analisis & Rekomendasi Sistem</h3>
    """
    if t_masuk == 0:
        html_insight += "<div style='padding: 15px; background-color: #E3F2FD; color: #0D47A1; border-radius: 8px; font-weight: 500;'>📌 Sistem belum menerima entri transaksi. Silakan input data pemasukan pertama.</div>"
    else:
        rasio = (t_keluar / t_masuk) * 100
        if rasio <= 40:
            html_insight += f"<div style='padding: 15px; background-color: #E8F5E9; color: #1B5E20; border-radius: 8px; font-weight: 500;'>✅ <b>STATUS AMAN (Realisasi: {rasio:.1f}%):</b> Kondisi kas sangat prima. Dana mencukupi untuk membiayai program kerja organisasi ke depan.</div>"
        elif rasio <= 75:
            html_insight += f"<div style='padding: 15px; background-color: #FFF3E0; color: #E65100; border-radius: 8px; font-weight: 500;'>⚠️ <b>STATUS PANTAU (Realisasi: {rasio:.1f}%):</b> Penyerapan anggaran cukup tinggi. Pastikan pengeluaran logistik tetap terkontrol oleh Bendahara.</div>"
        else:
            html_insight += f"<div style='padding: 15px; background-color: #FFEBEE; color: #B71C1C; border-radius: 8px; font-weight: 500;'>🚨 <b>STATUS KRITIS (Realisasi: {rasio:.1f}%):</b> Dana dewan hampir habis! Segera hentikan pengeluaran sekunder dan evaluasi sisa kas.</div>"
    html_insight += "</div>"
    st.markdown(html_insight, unsafe_allow_html=True)
    
    # VISUALISASI DATA LENGKAP
    if not df.empty:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("<h4 style='color: #5C4033; text-align: center;'>📊 Komposisi Pemasukan</h4>", unsafe_allow_html=True)
            df_masuk = df[df['jenis'] == 'Masuk']
            if not df_masuk.empty:
                fig_pie_in = px.pie(df_masuk, values='jumlah', names='kategori', hole=0.4, 
                                 color_discrete_sequence=['#4A3623', '#A67C52', '#D4A373', '#E8D8C8'])
                fig_pie_in.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie_in, use_container_width=True)
            else:
                st.caption("Belum ada rincian pemasukan.")
                
        with col_c2:
            st.markdown("<h4 style='color: #5C4033; text-align: center;'>📊 Komposisi Pengeluaran</h4>", unsafe_allow_html=True)
            df_keluar = df[df['jenis'] == 'Keluar']
            if not df_keluar.empty:
                fig_pie_out = px.pie(df_keluar, values='jumlah', names='kategori', hole=0.4, 
                                 color_discrete_sequence=['#5C4033', '#8B5A2B', '#C89F70', '#E0D4C8'])
                fig_pie_out.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie_out, use_container_width=True)
            else:
                st.caption("Belum ada rincian pengeluaran.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #5C4033;'>📈 Tren Arus Kas Harian</h4>", unsafe_allow_html=True)
        df_trend = df.groupby(['tanggal', 'jenis'])['jumlah'].sum().reset_index()
        fig_bar = px.bar(df_trend, x='tanggal', y='jumlah', color='jenis', barmode='group', 
                         color_discrete_map={'Masuk': '#C89F70', 'Keluar': '#3E2723'},
                         labels={'jumlah': 'Nominal (Rp)', 'tanggal': 'Tanggal Transaksi', 'jenis': 'Jenis'})
        fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# --- MENU 2: INPUT TRANSAKSI ---
# ==========================================
elif menu_pilihan == "📝 Input Transaksi":
    st.markdown("<h1 style='color: #3E2723; font-weight: 800; margin-bottom: 25px;'>Input Transaksi Baru</h1>", unsafe_allow_html=True)
    
    with st.container():
        jenis_input = st.radio("Pilih Jenis Transaksi:", ["Pemasukan", "Pengeluaran"], horizontal=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("form_racana", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            
            with col_a:
                deskripsi_input = st.text_input("Keterangan Sumber/Tujuan Dana*", placeholder="Masukkan detail transaksi...")
                jumlah_input = st.number_input("Nominal Transaksi (Rp)*", min_value=0, step=10000)
                
            with col_b:
                if jenis_input == "Pemasukan":
                    kategori_input = st.selectbox("Kategori Klasifikasi", KATEGORI_MASUK)
                else:
                    kategori_input = st.selectbox("Kategori Klasifikasi", KATEGORI_KELUAR)
                tanggal_input = st.date_input("Tanggal Transaksi")

            file_nota = None
            if jenis_input == "Pengeluaran":
                st.markdown("---")
                file_nota = st.file_uploader("🧾 Upload Bukti Pembayaran / Nota (Opsional)", type=['png', 'jpg', 'jpeg'])

            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("Simpan Transaksi ke Sistem", use_container_width=True, type="primary")
            
            if submit_btn:
                if not deskripsi_input or jumlah_input <= 0:
                    st.error("⚠️ Gagal: Deskripsi dan nominal wajib diisi dengan benar.")
                else:
                    path_nota_tersimpan = None
                    if jenis_input == "Pengeluaran" and file_nota is not None:
                        if not os.path.exists("nota_uploads"):
                            os.makedirs("nota_uploads")
                        path_nota_tersimpan = os.path.join("nota_uploads", file_nota.name)
                        with open(path_nota_tersimpan, "wb") as f:
                            f.write(file_nota.getbuffer())

                    if jenis_input == "Pemasukan":
                        tx = Pemasukan(deskripsi_input, jumlah_input, kategori_input, tanggal_input)
                    else:
                        tx = Pengeluaran(deskripsi_input, jumlah_input, kategori_input, tanggal_input, path_nota_tersimpan)
                    
                    manager.catat_transaksi(tx)
                    st.success("✅ Transaksi berhasil dicatat!")
                    st.rerun()

# ==========================================
# --- MENU 3: AUDIT & RIWAYAT ---
# ==========================================
elif menu_pilihan == "🔍 Audit & Riwayat":
    st.markdown("<h1 style='color: #3E2723; font-weight: 800; margin-bottom: 25px;'>Buku Besar & Audit</h1>", unsafe_allow_html=True)
    
    if df.empty:
        st.info("Belum ada data transaksi yang tersimpan di dalam database.")
    else:
        df_tampil = df.drop(columns=['bukti_nota'], errors='ignore')
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_audit1, col_audit2 = st.columns(2)
        
        with col_audit1:
            st.markdown("<div class='data-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #5C4033;'>🧾 Cek Bukti Nota</h3>", unsafe_allow_html=True)
            id_cek = st.number_input("Masukkan ID Transaksi:", min_value=1, step=1, key="cek")
            if st.button("Lihat Dokumen", use_container_width=True):
                cek_data = df[df['id'] == id_cek]
                if cek_data.empty:
                    st.warning("ID Transaksi tidak ditemukan.")
                elif cek_data.iloc[0]['jenis'] == "Masuk":
                    st.info("Pemasukan tidak memiliki bukti nota belanja.")
                else:
                    path_foto = cek_data.iloc[0]['bukti_nota']
                    if path_foto and os.path.exists(path_foto):
                        st.image(path_foto, caption=f"Nota Transaksi ID: {id_cek}", use_container_width=True)
                    else:
                        st.error("Tidak ada file nota yang diunggah untuk ID ini.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_audit2:
            st.markdown("<div class='data-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #5C4033;'>🗑️ Hapus Transaksi</h3>", unsafe_allow_html=True)
            id_hapus = st.number_input("Masukkan ID Transaksi:", min_value=1, step=1, key="hapus")
            if st.button("Hapus Permanen", use_container_width=True, type="primary"):
                manager.hapus_transaksi(id_hapus)
                st.success(f"Data dengan ID {id_hapus} berhasil dihapus.")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)