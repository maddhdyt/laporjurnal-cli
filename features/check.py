import os
import pandas as pd

class CekJurnal:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def cek_jurnal(self):
        """Fungsi untuk mengecek status jurnal"""
        self.clear_screen()
        print("\n=== Cek Status Jurnal ===")
        
        # Minta input URL dari pengguna
        url = input("Masukkan URL jurnal: ")
        
        # Membaca data dari file Excel
        try:
            df = pd.read_excel('c:\\Users\\Kautsar\\Documents\\Kulyeah\\laporjurnal-cli\\db_file.xlsx')
        except Exception as e:
            print(f"Terjadi kesalahan saat membaca file: {e}")
            return
        
        # Mencari data jurnal berdasarkan URL
        jurnal_data = df[df['url_jurnal'] == url]
        
        if jurnal_data.empty:
            print("Data jurnal tidak ditemukan untuk URL yang diberikan.")
        else:
            # Ambil data dari DataFrame
            for index, row in jurnal_data.iterrows():
                print("\nInformasi Jurnal:")
                print(f"ID Laporan: {row['id_laporan']}")
                print(f"Tanggal Pelaporan: {row['tanggal_pelaporan']}")
                print(f"Nama Jurnal: {row['nama_jurnal']}")
                print(f"URL Jurnal: {row['url_jurnal']}")
                print(f"Nama Pelapor: {row['nama_pelapor']}")
                print(f"Instansi Pelapor: {row['instansi_pelapor']}")
                print(f"Alasan Melapor: {row['alasan_melapor']}")
                print(f"Nama Validator: {row['nama_validator']}")
                print(f"Profile Validator: {row['profile_validator']}")
                print(f"Feedback: {row['feedback']}")
        
        input("\nTekan Enter untuk kembali ke menu...")