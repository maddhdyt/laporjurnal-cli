import pandas as pd
import os

class UserModel:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):  # Jika file tidak ada, buat file baru
            self.create_file()

    def create_file(self):
        """Membuat file Excel baru dengan header default."""
        if "validator" in self.file_path:
            columns = ["validator_id", "username", "password", "full_name", "email", "instancy", "academic_position", "scopus_url", "sinta_url", "google_scholar_url"]
        else:
            columns = ["user_id", "username", "password", "full_name", "email", "instancy", "role"]
        pd.DataFrame(columns=columns).to_excel(self.file_path, index=False, engine="openpyxl")

    def read_data(self):
        """Membaca data dari file Excel."""
        try:
            return pd.read_excel(self.file_path, engine="openpyxl")
        except FileNotFoundError:
            self.create_file()
            return pd.read_excel(self.file_path, engine="openpyxl")
        except Exception as e:
            print(f"Error reading file: {e}")
            return pd.DataFrame()

    def write_data(self, data):
        """Menulis data ke file Excel."""
        data.to_excel(self.file_path, index=False, engine="openpyxl")

    def add_user(self, user_data):
        """Menambahkan user baru ke file Excel."""
        try:
            # Baca data dari file Excel
            data = pd.read_excel(self.file_path, engine="openpyxl")
        except FileNotFoundError:
            # Jika file tidak ada, buat file baru dengan kolom yang sesuai
            columns = ["validator_id", "username", "password", "full_name", "email", "instancy", "academic_position", "scopus_url", "sinta_url", "google_scholar_url"]
            data = pd.DataFrame(columns=columns)

        # Tambahkan data user baru
        new_data = pd.DataFrame([user_data])
        data = pd.concat([data, new_data], ignore_index=True)

        # Simpan kembali ke file Excel
        data.to_excel(self.file_path, index=False, engine="openpyxl")

