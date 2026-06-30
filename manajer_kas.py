import database

class KasManager:
    def __init__(self):
        # Otomatis membuat tabel jika belum ada
        database.setup_database()

    def catat_transaksi(self, objek_transaksi):
        sql = "INSERT INTO transaksi (jenis, deskripsi, jumlah, kategori, tanggal, bukti_nota) VALUES (?, ?, ?, ?, ?, ?)"
        params = (objek_transaksi.jenis, objek_transaksi.deskripsi, objek_transaksi.jumlah, 
                  objek_transaksi.kategori, objek_transaksi.tanggal.strftime("%Y-%m-%d"), objek_transaksi.bukti_nota)
        return database.execute_query(sql, params)

    def hapus_transaksi(self, id_transaksi):
        sql = "DELETE FROM transaksi WHERE id = ?"
        return database.execute_query(sql, (id_transaksi,))

    def get_semua_data(self):
        sql = "SELECT id, tanggal, jenis, kategori, deskripsi, jumlah, bukti_nota FROM transaksi ORDER BY tanggal DESC, id DESC"
        return database.get_dataframe(sql)

    def get_ringkasan(self):
        df = self.get_semua_data()
        if df.empty:
            return 0, 0, 0, df
        
        # Menghitung otomatis menggunakan Pandas
        total_masuk = df[df['jenis'] == 'Masuk']['jumlah'].sum()
        total_keluar = df[df['jenis'] == 'Keluar']['jumlah'].sum()
        saldo = total_masuk - total_keluar
        return total_masuk, total_keluar, saldo, df