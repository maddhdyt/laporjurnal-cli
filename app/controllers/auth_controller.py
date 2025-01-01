import pandas as pd
from app.models.user_model import CSVModel
import re

class AuthController:
    def __init__(self):
        self.current_user = None
        self.user_model = CSVModel("database/tb_user.csv")
        self.validator_model = CSVModel("database/tb_validator.csv")
        self.admin_model = CSVModel("database/tb_admin.csv")

    def login(self):
        """Proses login multi-role dengan pesan kesalahan yang jelas."""
        print("\n=== Login ===")

        while True:  # Loop untuk mencoba kembali jika login gagal
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            try:
                # Periksa user
                user_data = self.user_model.read_data()
                user = user_data[user_data["username"] == username]
                if not user.empty:
                    if user.iloc[0]["password"] == password:
                        self.current_user = user.iloc[0].to_dict()
                        print(f"Login successful! Welcome, {username} (User).")
                        return "user"
                    else:
                        print("Invalid password. Please try again.")
                        continue

                # Periksa validator
                validator_data = self.validator_model.read_data()
                validator = validator_data[validator_data["username"] == username]
                if not validator.empty:
                    if validator.iloc[0]["password"] == password:
                        self.current_user = validator.iloc[0].to_dict()
                        print(f"Login successful! Welcome, {username} (Validator).")
                        return "validator"
                    else:
                        print("Invalid password. Please try again.")
                        continue

                # Periksa admin
                admin_data = self.admin_model.read_data()
                admin = admin_data[admin_data["username"] == username]
                if not admin.empty:
                    if admin.iloc[0]["password"] == password:
                        self.current_user = admin.iloc[0].to_dict()
                        print(f"Login successful! Welcome, {username} (Admin).")
                        return "admin"
                    else:
                        print("Invalid password. Please try again.")
                        continue

                # Jika username tidak ditemukan
                print("Invalid username. Please try again.")
            except Exception as e:
                print(f"Error: {e}")
                return None

    def register_user(self):
        """Proses registrasi user."""
        print("\n=== Register User ===")

        # Validasi Username
        while True:
            username = input("Enter username: ").strip()
            if not self.is_valid_username(username):
                print("Username must be at least 8 characters and can only contain letters, numbers, '_', and '.'.")
                continue
            # Cek apakah username sudah ada
            user_data = self.user_model.read_data()
            if not user_data[user_data["username"] == username].empty:
                print("Username already exists. Please choose another one.")
                continue
            break

        # Validasi Password
        while True:
            password = input("Enter password: ").strip()
            if not self.is_valid_password(password):
                print("Password must be at least 8 characters.")
                continue
            break

        # Validasi Full Name
        full_name = input("Enter full name: ").strip()

        # Validasi Email
        while True:
            email = input("Enter email: ").strip()
            if not self.is_valid_email(email):
                print("Invalid email format. Please try again.")
                continue
            break

        # Validasi Instancy
        instancy = input("Enter instancy: ").strip()

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
        print("Registration successful!")
    
    def register_validator(self):
        """Proses registrasi validator (hanya bisa dilakukan oleh admin)."""
        print("\n=== Register Validator ===")

        # Validasi Username
        while True:
            username = input("Enter username: ").strip()
            if not self.is_valid_username(username):
                print("Username must be at least 8 characters and can only contain letters, numbers, '_', and '.'.")
                continue
            # Cek apakah username sudah ada
            validator_data = self.validator_model.read_data()
            if not validator_data[validator_data["username"] == username].empty:
                print("Username already exists. Please choose another one.")
                continue
            break

        # Validasi Password
        while True:
            password = input("Enter password: ").strip()
            if not self.is_valid_password(password):
                print("Password must be at least 8 characters.")
                continue
            break

        # Validasi Full Name
        full_name = input("Enter full name: ").strip()

        # Validasi Email
        while True:
            email = input("Enter email: ").strip()
            if not self.is_valid_email(email):
                print("Invalid email format. Please try again.")
                continue
            break

        # Validasi Instancy
        instancy = input("Enter instancy: ").strip()

        # Validasi Academic Position
        academic_position = input("Enter academic position: ").strip()

        # Validasi Scopus URL
        while True:
            scopus_url = input("Enter Scopus URL: ").strip()
            if not scopus_url.startswith("http"):
                print("Invalid Scopus URL. Please enter a valid URL starting with 'http'.")
                continue
            break

        # Validasi Sinta URL
        while True:
            sinta_url = input("Enter Sinta URL: ").strip()
            if not sinta_url.startswith("http"):
                print("Invalid Sinta URL. Please enter a valid URL starting with 'http'.")
                continue
            break

        # Validasi Google Scholar URL
        while True:
            google_scholar_url = input("Enter Google Scholar URL: ").strip()
            if not google_scholar_url.startswith("http"):
                print("Invalid Google Scholar URL. Please enter a valid URL starting with 'http'.")
                continue
            break

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
        print("Validator registration successful!")
        
    def delete_validator(self, validator_id):
        """Menghapus akun validator berdasarkan Validator ID."""
        try:
            # Baca data validator dari file CSV
            validator_data = self.validator_model.read_data()
    
            # Filter data untuk menghapus baris dengan validator_id yang sesuai
            validator_data = validator_data[validator_data["validator_id"] != validator_id]
    
            # Simpan kembali data yang sudah dihapus ke file CSV
            self.validator_model.write_data(validator_data)
            print(f"Validator with ID {validator_id} has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting validator: {e}")

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
    
    def user_settings(self):
        """Fitur untuk mengedit informasi user dan mengubah password."""
        if not self.current_user:
            print("You must be logged in to access settings.")
            return

        while True:
            print("\n=== User Settings ===")
            print("1. Edit Profile Information")
            print("2. Change Password")
            print("3. Return to User Menu")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.edit_profile()
            elif choice == "2":
                self.change_password()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    def edit_profile(self):
        """Mengedit informasi profil user."""
        print("\n=== Edit Profile ===")
        user_data = self.user_model.read_data()
        user_id = self.current_user["user_id"]
        user = user_data[user_data["user_id"] == user_id].iloc[0]

        # Tampilkan informasi saat ini
        print(f"Current Full Name: {user['full_name']}")
        print(f"Current Email: {user['email']}")
        print(f"Current Instancy: {user['instancy']}")

        # Input untuk mengedit informasi
        new_full_name = input("Enter new full name (leave blank to keep current): ").strip()
        new_email = input("Enter new email (leave blank to keep current): ").strip()
        new_instancy = input("Enter new instancy (leave blank to keep current): ").strip()

        # Update informasi jika input tidak kosong
        if new_full_name:
            user_data.loc[user_data["user_id"] == user_id, "full_name"] = new_full_name
        if new_email:
            user_data.loc[user_data["user_id"] == user_id, "email"] = new_email
        if new_instancy:
            user_data.loc[user_data["user_id"] == user_id, "instancy"] = new_instancy

        # Simpan perubahan
        self.user_model.write_data(user_data)
        print("Profile updated successfully.")

    def change_password(self):
        """Mengubah password user."""
        print("\n=== Change Password ===")
        user_data = self.user_model.read_data()
        user_id = self.current_user["user_id"]
        user = user_data[user_data["user_id"] == user_id].iloc[0]

        # Minta password lama untuk verifikasi
        old_password = input("Enter your current password: ").strip()
        if old_password != user["password"]:
            print("Incorrect password. Please try again.")
            return

        # Minta password baru
        while True:
            new_password = input("Enter new password: ").strip()
            if self.is_valid_password(new_password):
                break
            else:
                print("Password must be at least 8 characters.")

        # Update password
        user_data.loc[user_data["user_id"] == user_id, "password"] = new_password
        self.user_model.write_data(user_data)
        print("Password changed successfully.")
