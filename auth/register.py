import pandas as pd
import hashlib
import re
from datetime import datetime
from pathlib import Path
import os
import time

class Register:
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
                time.sleep(1)  # Tunggu 1 detik sebelum mencoba lagi
    
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
                time.sleep(1)  # Tunggu 1 detik sebelum mencoba lagi
    
    def hash_password(self, password):
        """Hash password menggunakan SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_email(self, email):
        """Validasi format email"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def validate_username(self, username):
        """Validasi username (minimal 4 karakter, hanya alfanumerik)"""
        return len(username) >= 4 and username.isalnum()
    
    def validate_password(self, password):
        """Validasi password (minimal 6 karakter)"""
        return len(password) >= 6
    
    def username_exists(self, username):
        """Cek apakah username sudah ada"""
        df = self.load_dataframe()
        return username in df['username'].values
    
    def email_exists(self, email):
        """Cek apakah email sudah ada"""
        df = self.load_dataframe()
        return email in df['email'].values
    
    def register(self):
        """Proses registrasi user baru"""
        print("\n=== REGISTER laporJurnal.id ===")
        while True:
            username = input("Username (min. 4 karakter, alfanumerik): ").strip()
            if not self.validate_username(username):
                print("Username tidak valid!")
                continue
            if self.username_exists(username):
                print("Username sudah digunakan!")
                continue
            break
        
        while True:
            email = input("Email: ").strip()
            if not self.validate_email(email):
                print("Format email tidak valid!")
                continue
            if self.email_exists(email):
                print("Email sudah terdaftar!")
                continue
            break
        
        while True:
            password = input("Password (min. 6 karakter): ").strip()
            if not self.validate_password(password):
                print("Password terlalu pendek!")
                continue
            confirm_password = input("Konfirmasi password: ").strip()
            if password != confirm_password:
                print("Password tidak cocok!")
                continue
            break
        
        full_name = input("Nama lengkap: ").strip()
        
        # Tambahkan user baru
        df = self.load_dataframe()
        new_user = {
            'username': username,
            'password': self.hash_password(password),
            'email': email,
            'full_name': full_name,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'role': 'user'
        }
        
        df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
        try:
            self.save_dataframe(df)
            print("\nRegistrasi berhasil! Silakan login.")
        except Exception as e:
            print(f"\nError: {str(e)}")