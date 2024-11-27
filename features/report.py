import os

class CekLaporan:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def cek_laporan(self):
        """Fungsi untuk mengecek laporan"""
        self.clear_screen()
        print("\n=== Cek Laporan ===")
        # Tambahkan kode untuk cek laporan di sini
        input("\nFitur ini masih dalam pengembangan. Tekan Enter untuk kembali ke menu...")