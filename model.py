from datetime import date

# Parent Class
class Transaksi:
    # Parameter bukti_nota ditambahkan dengan default None
    def __init__(self, deskripsi, jumlah, kategori, tgl=None, bukti_nota=None):
        self.deskripsi = deskripsi
        self.jumlah = float(jumlah)
        self.kategori = kategori
        self.tanggal = tgl if tgl else date.today()
        self.bukti_nota = bukti_nota

# Child Class 1 (Pemasukan TIDAK pakai nota)
class Pemasukan(Transaksi):
    def __init__(self, deskripsi, jumlah, kategori, tgl=None):
        # super() mengirimkan None untuk bukti_nota
        super().__init__(deskripsi, jumlah, kategori, tgl, None)
        self.jenis = "Masuk"

# Child Class 2 (Pengeluaran PAKAI nota)
class Pengeluaran(Transaksi):
    def __init__(self, deskripsi, jumlah, kategori, tgl=None, bukti_nota=None):
        super().__init__(deskripsi, jumlah, kategori, tgl, bukti_nota)
        self.jenis = "Keluar"