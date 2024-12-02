from auth.auth import Authentication
from features.lapor import LaporJurnal
from features.check import CekJurnal
from features.report import CekLaporan
import os

def clear_screen():
    """Membersihkan layar terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_main_menu(user):
    """Menampilkan menu utama setelah login"""
    # Inisialisasi objek fitur
    lapor = LaporJurnal()
    check = CekJurnal()
    report = CekLaporan()

    while True:
        clear_screen()
        print(f"\n=== laporJurnal.id - Selamat datang, {user['full_name']} ===")
        print("1. Lapor Jurnal")
        print("2. Cek Jurnal")
        print("3. Cek Laporan")
        print("4. Logout")
        
        choice = input("\nPilih menu (1-4): ").strip()
        
        if choice == "1":
            lapor.lapor_jurnal(user)  # Mengirim user sebagai current_user
        elif choice == "2":
            check.cek_jurnal()
        elif choice == "3":
            report.cek_laporan()
        elif choice == "4":
            print("\nAnda telah logout. Terima kasih!")
            break
        else:
            input("\nMenu tidak valid! Tekan Enter untuk melanjutkan...")

def show_auth_menu():
    """Menampilkan menu autentikasi"""
    while True:
        clear_screen()
        print("\n=== laporJurnal.id ===")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")
        
        choice = input("\nPilih menu (1-3): ").strip()
        
        if choice == "1":
            return "login"
        elif choice == "2":
            return "register"
        elif choice == "3":
            return "exit"
        else:
            input("\nMenu tidak valid! Tekan Enter untuk melanjutkan...")

def main():
    auth = Authentication()
    
    while True:
        auth_choice = show_auth_menu()
        
        if auth_choice == "login":
            user = auth.start_login()
            if user is not None:
                show_main_menu(user)
        elif auth_choice == "register":
            auth.start_register()
            input("\nTekan Enter untuk kembali ke menu...")
        elif auth_choice == "exit":
            clear_screen()
            print("\nTerima kasih telah menggunakan laporJurnal.id")
            break

if __name__ == "__main__":
    main()