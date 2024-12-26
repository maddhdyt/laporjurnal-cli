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
