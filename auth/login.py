import pandas as pd
import hashlib
from pathlib import Path
import os
import time

class Login:
    def __init__(self):
        self.file_path = Path('db/db_file.xlsx')
        # Buat folder db jika belum ada
        os.makedirs(self.file_path.parent, exist_ok=True)
        
        # Buat file Excel jika belum ada
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=['username', 'password', 'email', 'full_name', 'created_at', 'role'])
            self.save_dataframe(df)
    
    def load_dataframe(self):
        """Load data dari Excel dengan handling untuk file yang sedang digunakan"""
        max_attempts = 3
        current_attempt = 0
        while current_attempt < max_attempts:
            try:
                return pd.read_excel(self.file_path)
            except PermissionError:
                current_attempt += 1
                if current_attempt == max_attempts:
                    raise Exception("Tidak dapat mengakses database. Pastikan file Excel tidak sedang dibuka.")
                time.sleep(1)
    
    def save_dataframe(self, df):
        """Simpan dataframe ke Excel dengan handling untuk file yang sedang digunakan"""
        max_attempts = 3
        current_attempt = 0
        while current_attempt < max_attempts:
            try:
                df.to_excel(self.file_path, index=False)
                return True
            except PermissionError:
                current_attempt += 1
                if current_attempt == max_attempts:
                    raise Exception("Tidak dapat menyimpan ke database. Pastikan file Excel tidak sedang dibuka.")
                time.sleep(1)
    
    def hash_password(self, password):
        """Hash password menggunakan SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        """Proses login user"""
        try:
            df = self.load_dataframe()
            
            print("\n=== LOGIN laporJurnal.id ===")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            user = df[df['username'] == username]
            if user.empty:
                print("Username tidak ditemukan!")
                return None
            
            if user.iloc[0]['password'] == self.hash_password(password):
                print(f"\nSelamat datang, {user.iloc[0]['full_name']}!")
                return user.iloc[0]
            else:
                print("Password salah!")
                return None
        except Exception as e:
            print(f"\nError: {str(e)}")
            return None