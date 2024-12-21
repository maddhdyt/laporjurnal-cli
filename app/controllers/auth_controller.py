import re
import pandas as pd
from app.models.user_model import UserModel
from app.views.auth_view import show_register_user, show_register_validator, show_login

class AuthController:
    def __init__(self):
        self.current_user = None  # Simpan informasi user yang sedang login
        self.user_model = UserModel("database/tb_user.xlsx")
        self.validator_model = UserModel("database/tb_validator.xlsx")
        self.setup_default_admin()

    def setup_default_admin(self):
        data = self.user_model.read_data()
        if "admin" not in data["username"].values:
            default_admin = {
                "user_id": 1,
                "username": "admin",
                "password": "admin123",
                "full_name": "Default Admin",
                "email": "admin@example.com",
                "instancy": "System",
                "role": "admin",
            }
            self.user_model.add_user(default_admin)

    def is_valid_username(self, username):
        pattern = r"^[a-zA-Z0-9_.]{8,}$"
        return re.match(pattern, username) is not None

    def is_valid_password(self, password):
        return len(password) >= 8

    def is_valid_email(self, email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$"
        return re.fullmatch(pattern, email) is not None

    def is_valid_url(self, url):
        pattern = r"^(https?:\/\/)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(/[a-zA-Z0-9-._~:/?#[\]@!$&'()*+,;=]*)?$"
        return re.fullmatch(pattern, url) is not None

    def is_unique_username(self, username, model):
        data = model.read_data()
        return username not in data["username"].values

    def get_current_user_id(self):
        """Mengembalikan user_id pengguna yang sedang login."""
        if self.current_user and "user_id" in self.current_user:
            return self.current_user["user_id"]
        else:
            print("No user is currently logged in.")
            return None

    def register_user(self):
        """Registrasi user biasa."""
        show_register_user()

        # Input username dengan validasi
        while True:
            username = input("Enter username: ")
            if not self.is_valid_username(username):
                print("Username must be at least 8 characters, and can only contain letters, numbers, '_', and '.'.")
                continue

            if not self.is_unique_username(username, self.user_model):
                print("Username already exists. Please choose another one.")
                continue
            break

        # Input password dengan validasi
        while True:
            password = input("Enter password: ")
            if not self.is_valid_password(password):
                print("Password must be at least 8 characters.")
                continue
            break

        # Input full name (tidak perlu validasi tambahan)
        full_name = input("Enter full name: ")

        # Input email dengan validasi
        while True:
            email = input("Enter email: ")
            if not self.is_valid_email(email):
                print("Invalid email format. Please enter a valid email.")
                continue
            break

        # Input instansi (tidak perlu validasi tambahan)
        instancy = input("Enter instancy: ")

        # Jika semua validasi berhasil, tambahkan data ke database
        new_user = {
            "user_id": len(self.user_model.read_data()) + 1,
            "username": username,
            "password": password,
            "full_name": full_name,
            "email": email,
            "instancy": instancy,
            "role": "user",
        }

        self.user_model.add_user(new_user)
        print("User registration successful!")

    def register_validator(self):
        show_register_validator()
        while True:
            username = input("Enter username: ")
            if not self.is_valid_username(username):
                print("Username must be at least 8 characters, and can only contain letters, numbers, '_', and '.'.")
                continue

            if not self.is_unique_username(username, self.validator_model):
                print("Username already exists. Please choose another one.")
                continue

            password = input("Enter password: ")
            if not self.is_valid_password(password):
                print("Password must be at least 8 characters.")
                continue

            full_name = input("Enter full name: ")

            email = input("Enter email: ")
            if not self.is_valid_email(email):
                print("Invalid email format. Please enter a valid email.")
                continue

            instancy = input("Enter instancy: ")
            academic_position = input("Enter academic position: ")

            scopus_url = input("Enter Scopus URL: ")
            if not self.is_valid_url(scopus_url):
                print("Invalid Scopus URL. Please enter a valid URL.")
                continue

            sinta_url = input("Enter SINTA URL: ")
            if not self.is_valid_url(sinta_url):
                print("Invalid SINTA URL. Please enter a valid URL.")
                continue

            google_scholar_url = input("Enter Google Scholar URL: ")
            if not self.is_valid_url(google_scholar_url):
                print("Invalid Google Scholar URL. Please enter a valid URL.")
                continue

            new_validator = {
                "validator_id": len(self.validator_model.read_data()) + 1,
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

            self.validator_model.add_user(new_validator)
            print("Validator registration successful!")
            break

    def login(self):
        """Proses login untuk semua role."""
        show_login()

        while True:
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            # Baca data user
            user_data = self.user_model.read_data()
            validator_data = self.validator_model.read_data()

            # Normalisasi data (hapus spasi tambahan)
            user_data["username"] = user_data["username"].str.strip()
            user_data["password"] = user_data["password"].astype(str).str.strip()
            validator_data["username"] = validator_data["username"].str.strip()
            validator_data["password"] = validator_data["password"].astype(str).str.strip()

            # Gabungkan data user dan validator
            all_data = pd.concat([user_data, validator_data], ignore_index=True)

            # Cek username yang cocok
            matched_users = all_data[all_data["username"] == username]
            print("Matched Users by Username:")
            print(matched_users)

            # Cek password yang cocok
            user = matched_users[matched_users["password"] == password]
            if not user.empty:
                self.current_user = user.iloc[0].to_dict()
                role = self.current_user["role"]
                print(f"Login successful! Welcome, {self.current_user['full_name']} ({role.capitalize()}).")
                return role
            else:
                if not matched_users.empty:
                    print("Password mismatch for username:", username)
                print("Invalid username or password. Please try again.\n")







