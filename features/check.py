import os

class CekJurnal:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def cek_jurnal(self):
        """Fungsi untuk mengecek status jurnal"""
        self.clear_screen()
        print("\n=== Cek Status Jurnal ===")
        # Tambahkan kode untuk cek jurnal di sini
        input("\nFitur ini masih dalam pengembangan. Tekan Enter untuk kembali ke menu...")