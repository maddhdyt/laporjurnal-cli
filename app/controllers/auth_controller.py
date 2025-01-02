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
        print("\n=== Login ===")

        while True:
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
                        time.sleep(2)
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
                        print(f"Login successful! Welcome, {username} (Validator). Redirecting...")
                        time.sleep(2)
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
                        time.sleep(2)
                        return "admin"
                    else:
                        print("Invalid password. Please try again.")
                        continue

                print("Invalid username. Please try again.")
            except Exception as e:
                print(f"Error: {e}")
                return None

    def register_user(self):
        clear_screen()
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
        clear_screen()
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
        while True:
            full_name = input("Enter full name: ").strip()
            if not full_name:
                print("Full name cannot be empty. Please try again.")
            else:
                break
            
        # Validasi Email
        while True:
            email = input("Enter email: ").strip()
            if not self.is_valid_email(email):
                print("Invalid email format. Please try again.")
                continue
            break

        # Validasi Instancy
        while True:
            instancy = input("Enter instancy: ").strip()
            if not instancy:
                print("Instancy cannot be empty. Please try again.")
            else:
                break

        # Validasi Academic Position
        while True:
            academic_position = input("Enter academic position: ").strip()
            if not academic_position:
                print("Academic position cannot be empty. Please try again.")
            else:
                break

        # Opsi untuk menginput URL (Scopus, Sinta, Google Scholar)
        scopus_url = ""
        sinta_url = ""
        google_scholar_url = ""

        while True:
            print("\nDo you want to add URLs?")
            print("1. Add Scopus URL")
            print("2. Add Sinta URL")
            print("3. Add Google Scholar URL")
            print("4. Skip URL input")
            url_choice = input("Choose an option: ").strip()

            if url_choice == "1":
                scopus_url = self.get_valid_url("Scopus", "")
            elif url_choice == "2":
                sinta_url = self.get_valid_url("Sinta", "")
            elif url_choice == "3":
                google_scholar_url = self.get_valid_url("Google Scholar", "")
            elif url_choice == "4":
                break  # Keluar dari loop jika tidak ingin menginput URL
            else:
                print("Invalid choice. Please try again.")

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

    # User Setting Functionality
    def user_settings(self):
        """Fitur untuk mengedit informasi user dan mengubah password."""
        if not self.current_user:
            print("You must be logged in to access settings.")
            return
        
        clear_screen()

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
        
        # Validasi email baru
        while True:
            new_email = input("Enter new email (leave blank to keep current): ").strip()
            if new_email:  # Jika pengguna memasukkan email baru
                if not self.is_valid_email(new_email):  # Validasi email
                    print("Invalid email format. Please enter a valid email address (e.g., example@domain.com).")
                else:
                    break  # Keluar dari loop jika email valid
            else:
                break  # Keluar dari loop jika pengguna tidak memasukkan email baru

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
        """Meminta input URL yang valid untuk Scopus, Sinta, atau Google Scholar."""
        while True:
            print(f"\nCurrent {url_type} URL: {current_url}")
            new_url = input(f"Enter new {url_type} URL (or leave blank to keep current): ").strip()

            # Jika pengguna tidak memasukkan URL, kembalikan URL saat ini
            if not new_url:
                return current_url

            # Validasi URL
            if not new_url.startswith(("http://", "https://")):
                print(f"Invalid {url_type} URL. It must start with 'http://' or 'https://'.")
                continue
            if not new_url.endswith((".com", ".org", ".edu", ".gov", ".net", ".io", ".co.id")):
                print(f"Invalid {url_type} URL. It must end with a valid domain (e.g., .com, .org, .edu).")
                continue
            if len(new_url) < 10:
                print(f"Invalid {url_type} URL. It must be at least 10 characters long.")
                continue
            return new_url  # Kembalikan URL yang valid jika semua validasi terpenuhi   


