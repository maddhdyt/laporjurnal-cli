import os
import re

class LaporJurnal:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def is_valid_url(url):
        # Validasi format URL menggunakan regex
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// atau https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ... atau ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ... atau ipv6
            r'(?::\d+)?'  # port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)  # path
        return re.match(regex, url) is not None

    def lapor_jurnal(self):
        """Fungsi untuk melaporkan jurnal predator"""
        self.clear_screen()
        print("\n=== Lapor Jurnal Predator ===")
        
        link_jurnal = input("Masukkan link website jurnal yang ingin dilaporkan: ").strip()
        
        if not self.is_valid_url(link_jurnal):
            print("URL yang Anda masukkan tidak valid. Silakan coba lagi.")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        # Simulasi penyimpanan data
        with open("laporan_jurnal.txt", "a") as file:
            file.write(f"{link_jurnal}\n")
        
        print(f"Anda telah melaporkan jurnal dengan link: {link_jurnal}")
        print("Laporan Anda telah disimpan.")
        
        input("\nTekan Enter untuk kembali ke menu...")