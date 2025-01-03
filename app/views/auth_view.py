from utils import clear_screen

def show_main_menu():
    clear_screen()
    print("\n=== Menu Utama ===")
    print("1. Masuk")
    print("2. Daftar")
    print("3. Periksa URL Jurnal")
    print("4. Keluar")

def show_user_menu():
    clear_screen()
    print("\n=== Menu Pengguna ===")
    print("1. Laporkan Jurnal")
    print("2. Lacak Laporan")
    print("3. Pengaturan") 
    print("4. Keluar")

def show_validator_menu():
    clear_screen()
    print("\n=== Menu Validator ===")
    print("1. Melihat Laporan Tertunda")
    print("2. Melihat Laporan yang Diterima")
    print("3. Keluar")

def show_admin_menu():
    clear_screen()
    print("\n=== Menu Admin ===")
    print("1. Daftar Validator")
    print("2. Lihat Semua Laporan")  
    print("3. Lihat Semua Pengguna")    
    print("4. Lihat Semua Validator") 
    print("5. Keluar")
