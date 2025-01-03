from utils import clear_screen
import pandas as pd
from app.models.CSVModel import CSVModel
import re
import time

class AuthController:
    def __init__(self):
        self.current_user = None
        self.user_model = CSVModel("database/tb_user.csv")
        self.validator_model = CSVModel("database/tb_validator.csv")
        self.admin_model = CSVModel("database/tb_admin.csv")

    def login(self):
        # Multi Role Login
        print("\n=== Masuk ===")

        while True:
            username = input("Masukkan Username: ").strip()
            password = input("Masukkan Password: ").strip()

            try:
                # Periksa user
                user_data = self.user_model.read_data()
                user = user_data[user_data["username"] == username]
                if not user.empty:
                    if user.iloc[0]["password"] == password:
                        self.current_user = user.iloc[0].to_dict()
                        print(f"Masuk berhasil! Selamat datang, {username} (User). Redirecting...")
                        time.sleep(2)
                        return "user"
                    else:
                        print("Password salah. Silakan coba lagi.")
                        continue

                # Periksa validator
                validator_data = self.validator_model.read_data()
                validator = validator_data[validator_data["username"] == username]
                if not validator.empty:
                    if validator.iloc[0]["password"] == password:
                        self.current_user = validator.iloc[0].to_dict()
                        print(f"Masuk berhasil! Selamat datang, {username} (Validator). Redirecting...")
                        time.sleep(2)
                        return "validator"
                    else:
                        print("Password salah. Silakan coba lagi.")
                        continue

                # Periksa admin
                admin_data = self.admin_model.read_data()
                admin = admin_data[admin_data["username"] == username]
                if not admin.empty:
                    if admin.iloc[0]["password"] == password:
                        self.current_user = admin.iloc[0].to_dict()
                        print(f"Masuk berhasil! Selamat datang, {username} (Admin). Redirecting...")
                        time.sleep(2)
                        return "admin"
                    else:
                        print("Password salah. Silakan coba lagi.")
                        continue

                print("Username tidak valid. Silakan coba lagi.")
            except Exception as e:
                print(f"Error: {e}")
                return None

    def register_user(self):
        clear_screen()
        print("\n=== Daftar Pengguna ===")

        while True:
            username = input("Masukkan username: ").strip()
            if not self.is_valid_username(username):
                print("Username harus terdiri dari minimal 8 karakter dan hanya boleh terdiri dari huruf, angka, '_', dan '.'")
                continue
            # Cek apakah username sudah ada
            user_data = self.user_model.read_data()
            if not user_data[user_data["username"] == username].empty:
                print("Nama pengguna sudah ada. Pilih nama pengguna yang lain.")
                continue
            break

        # Validasi Password
        while True:
            password = input("Masukkan password: ").strip()
            if not self.is_valid_password(password):
                print("Password harus terdiri dari minimal 8 karakter.")
                continue
            break

        # Validasi Full Name
        full_name = input("Masukkan nama lengkap: ").strip()

        # Validasi Email
        while True:
            email = input("Masukkan email: ").strip()
            if not self.is_valid_email(email):
                print("Format email tidak valid. Silakan coba lagi..")
                continue
            # Cek apakah email sudah digunakan oleh user lain
            user_data = self.user_model.read_data()
            if not user_data[user_data["email"] == email].empty:
                print("Email sudah digunakan. Silakan pilih email lain.")
                continue
            break

        # Validasi Instancy
        instancy = input("Masukkan instansi: ").strip()

        # Tambahkan user baru
        new_user = {
            "user_id": int(user_data["user_id"].max() + 1) if not user_data.empty else 1,
            "username": username,
            "password": password,
            "full_name": full_name,
            "email": email,
            "instancy": instancy,
            "role": "user"
        }
        user_data = pd.concat([user_data, pd.DataFrame([new_user])], ignore_index=True)
        self.user_model.write_data(user_data)
        print("Pendaftaran berhasil!")
    
    def register_validator(self):
        clear_screen()
        print("\n=== Daftar Validator ===")

        # Validasi Username
        while True:
            username = input("Masukkan username: ").strip()
            if not self.is_valid_username(username):
                print("Username harus terdiri dari minimal 8 karakter dan hanya boleh terdiri dari huruf, angka, '_', dan '.'")
                continue
            # Cek apakah username sudah ada
            validator_data = self.validator_model.read_data()
            if not validator_data[validator_data["username"] == username].empty:
                print("Nama pengguna sudah ada. Silakan pilih nama pengguna yang lain..")
                continue
            break

        # Validasi Password
        while True:
            password = input("Masukkan password: ").strip()
            if not self.is_valid_password(password):
                print("Password harus terdiri dari minimal 8 karakter.")
                continue
            break

        # Validasi Full Name
        while True:
            full_name = input("Masukkan nama lengkap: ").strip()
            if not full_name:
                print("Nama lengkap tidak boleh kosong. Silakan coba lagi.")
            else:
                break
            
        # Validasi Email
        while True:
            email = input("Masukkan email: ").strip()
            if not self.is_valid_email(email):
                print("Format email tidak valid. Silakan coba lagi..")
                continue
            # Cek apakah email sudah digunakan oleh user lain
            validator_data = self.validator_model.read_data()
            if not validator_data[validator_data["email"] == email].empty:
                print("Email sudah digunakan. Silakan pilih email lain..")
                continue
            break

        # Validasi Instancy
        while True:
            instancy = input("Masukkan instansi: ").strip()
            if not instancy:
                print("Instansi tidak boleh kosong. Silakan coba lagi..")
            else:
                break

        # Validasi Academic Position
        while True:
            academic_position = input("Masukkan posisi akademik: ").strip()
            if not academic_position:
                print("Posisi akademik tidak boleh kosong. Silakan coba lagi.")
            else:
                break

        # Input URL (Scopus, Sinta, Google Scholar) dengan rule get_valid_url
        scopus_url = self.get_valid_url("Scopus", "")
        sinta_url = self.get_valid_url("Sinta", "")
        google_scholar_url = self.get_valid_url("Google Scholar", "")

        # Tambahkan validator baru
        new_validator = {
            "validator_id": int(validator_data["validator_id"].max() + 1) if not validator_data.empty else 1,
            "username": username,
            "password": password,
            "full_name": full_name,
            "email": email,
            "instancy": instancy,
            "academic_position": academic_position,
            "scopus_url": scopus_url,
            "sinta_url": sinta_url,
            "google_scholar_url": google_scholar_url,
            "role": "validator"
        }
        validator_data = pd.concat([validator_data, pd.DataFrame([new_validator])], ignore_index=True)
        self.validator_model.write_data(validator_data)
        print("Pendaftaran validator berhasil!!")

    # User Setting Functionality
    def user_settings(self):
        """Fitur untuk mengedit informasi user dan mengubah password."""
        if not self.current_user:
            print("Anda harus login untuk mengakses pengaturan")
            return
        
        clear_screen()

        while True:
            print("\n=== Pengaturan Pengguna ===")
            print("1. Edit Informasi Profil")
            print("2. Ganti Password")
            print("3. Kembali ke Menu Pengguna")
            choice = input("Pilih opsi: ").strip()

            if choice == "1":
                self.edit_profile()
            elif choice == "2":
                self.change_password()
            elif choice == "3":
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi..")

    def edit_profile(self):
        """Mengedit informasi profil user."""
        print("\n=== Edit Informasi Profil ===")
        user_data = self.user_model.read_data()
        user_id = self.current_user["user_id"]
        user = user_data[user_data["user_id"] == user_id].iloc[0]

        # Tampilkan informasi saat ini
        print(f"Nama Lengkap Saat Ini: {user['full_name']}")
        print(f"Email Saat Ini: {user['email']}")
        print(f"Instansi Saat Ini: {user['instancy']}")

        # Input untuk mengedit informasi
        new_full_name = input("Masukkan nama lengkap baru (kosongkan untuk mempertahankan yang saat ini): ").strip()
        
        # Validasi email baru
        while True:
            new_email = input("Masukkan email baru (kosongkan untuk mempertahankan yang saat ini):: ").strip()
            if new_email:  # Jika pengguna memasukkan email baru
                if not self.is_valid_email(new_email):  # Validasi email
                    print("Format email tidak valid. Silakan masukkan alamat email yang valid (contoh: example@domain.com).")
                else:
                    break  # Keluar dari loop jika email valid
            else:
                break  # Keluar dari loop jika pengguna tidak memasukkan email baru

        new_instancy = input("Masukkan instansi baru (kosongkan untuk mempertahankan yang saat ini): ").strip()

        # Update informasi jika input tidak kosong
        if new_full_name:
            user_data.loc[user_data["user_id"] == user_id, "full_name"] = new_full_name
        if new_email:
            user_data.loc[user_data["user_id"] == user_id, "email"] = new_email
        if new_instancy:
            user_data.loc[user_data["user_id"] == user_id, "instancy"] = new_instancy

        # Simpan perubahan
        self.user_model.write_data(user_data)
        print("Profil berhasil diperbarui.")

    def change_password(self):
        """Mengubah password user."""
        print("\n=== Ganti Password ===")
        user_data = self.user_model.read_data()
        user_id = self.current_user["user_id"]
        user = user_data[user_data["user_id"] == user_id].iloc[0]

        # Minta password lama untuk verifikasi
        old_password = input("Masukkan password saat ini:: ").strip()
        if old_password != user["password"]:
            print("Password salah. Silakan coba lagi..")
            return

        # Minta password baru
        while True:
            new_password = input("Masukkan password baru: ").strip()
            if self.is_valid_password(new_password):
                break
            else:
                print("Password harus terdiri dari minimal 8 karakter.")

        # Update password
        user_data.loc[user_data["user_id"] == user_id, "password"] = new_password
        self.user_model.write_data(user_data)
        print("Password berhasil diubah.")
        
    # Validation Rule
    def is_valid_username(self, username):
        """Validasi username."""
        return re.match(r"^[a-zA-Z0-9_.]{8,}$", username)

    def is_valid_password(self, password):
        """Validasi password."""
        return len(password) >= 8

    def is_valid_email(self, email):
        """Validasi email menggunakan regex yang benar."""
        return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None

    def get_current_user_id(self):
        """Kembalikan user_id dari pengguna yang login."""
        if self.current_user:
            return self.current_user.get("user_id")
        return None

    def get_valid_url(self, url_type, current_url):
        while True:
            print(f"\nMasukkan {url_type} URL (harus dimulai dengan 'http://' atau 'https://', mengandung domain yang valid, dan minimal 10 karakter panjang):")
            new_url = input().strip()
            
            # Validasi URL
            if not new_url.startswith(("http://", "https://")):
                print(f"{url_type} URL tidak valid . Harus dimulai dengan 'http://' atau 'https://'.")
            elif not "." in new_url:  # Minimal harus ada domain (contoh: example.com)
                print(f"{url_type} URL tidak valid . Harus mengandung domain yang valid.")
            elif len(new_url) < 10:
                print(f"{url_type} URL tidak valid . Panjangnya minimal 10 karakter.")
            else:
                return new_url

