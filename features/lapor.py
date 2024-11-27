import os

class LaporJurnal:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def lapor_jurnal(self):
        """Fungsi untuk melaporkan jurnal predator"""
        self.clear_screen()
        print("\n=== Lapor Jurnal Predator ===")
        # Tambahkan kode untuk melapor jurnal di sini
        input("\nFitur ini masih dalam pengembangan. Tekan Enter untuk kembali ke menu...")