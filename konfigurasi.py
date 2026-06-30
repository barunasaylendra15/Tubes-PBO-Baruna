import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'buku_kas_racana.db')

# Kategori dinamis dan profesional khusus UKM Racana Pandawa
KATEGORI_MASUK = [
    "Iuran Wajib Anggota", 
    "Donasi & Sponsorship", 
    "Dana Alokasi Kampus (DIPA)", 
    "Usaha Mandiri (Kedai/Merch)", 
    "Lainnya"
]

KATEGORI_KELUAR = [
    "Operasional & Kesekretariatan", 
    "Pelaksanaan Proker (Event)", 
    "Perlengkapan & Adat Racana", 
    "Konsumsi & Rapat Dewan", 
    "Bantuan Sosial & Pengabdian"
]