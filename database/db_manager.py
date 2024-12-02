import pandas as pd
import os
from pathlib import Path
import time
from datetime import datetime
import uuid

class DatabaseManager:
    def __init__(self):
        self.file_path = Path('db/db_file.xlsx')
        os.makedirs(self.file_path.parent, exist_ok=True)
        self.initialize_database()
    
    def initialize_database(self):
        """Inisialisasi database jika belum ada"""
        if not os.path.exists(self.file_path):
            users_df = pd.DataFrame(columns=[
                'username', 'password', 'email', 'full_name', 'created_at', 'role'
            ])
            reports_df = pd.DataFrame(columns=[
                'report_id', 'journal_name', 'journal_url', 'reason', 
                'is_anonymous', 'reporter_username', 'status', 
                'created_at', 'updated_at'
            ])
            validations_df = pd.DataFrame(columns=[
                'validation_id', 'report_id', 'validator_username', 
                'status', 'feedback', 'created_at', 'updated_at'
            ])
            revision_history_df = pd.DataFrame(columns=[
                'revision_id', 'report_id', 'original_report', 
                'revision_note', 'created_at'
            ])
            
            with pd.ExcelWriter(self.file_path) as writer:
                users_df.to_excel(writer, sheet_name='users', index=False)
                reports_df.to_excel(writer, sheet_name='reports', index=False)
                validations_df.to_excel(writer, sheet_name='validations', index=False)
                revision_history_df.to_excel(writer, sheet_name='revision_history', index=False)

    def load_sheet(self, sheet_name):
        """Load specific sheet dari Excel dengan handling untuk file yang sedang digunakan"""
        max_attempts = 3
        current_attempt = 0
        while current_attempt < max_attempts:
            try:
                return pd.read_excel(self.file_path, sheet_name=sheet_name)
            except PermissionError:
                current_attempt += 1
                if current_attempt == max_attempts:
                    raise Exception(f"Tidak dapat mengakses sheet {sheet_name}. Pastikan file Excel tidak sedang dibuka.")
                time.sleep(1)

    def save_sheet(self, df, sheet_name):
        """Simpan dataframe ke sheet Excel dengan handling untuk file yang sedang digunakan"""
        max_attempts = 3
        current_attempt = 0
        while current_attempt < max_attempts:
            try:
                # Baca semua sheet yang ada
                with pd.ExcelFile(self.file_path) as xls:
                    sheets = {name: pd.read_excel(xls, name) for name in xls.sheet_names if name != sheet_name}
                
                # Tulis ulang semua sheet termasuk yang diupdate
                with pd.ExcelWriter(self.file_path) as writer:
                    for name, sheet_df in sheets.items():
                        sheet_df.to_excel(writer, name, index=False)
                    df.to_excel(writer, sheet_name, index=False)
                return True
            except PermissionError:
                current_attempt += 1
                if current_attempt == max_attempts:
                    raise Exception(f"Tidak dapat menyimpan ke sheet {sheet_name}. Pastikan file Excel tidak sedang dibuka.")
                time.sleep(1)

    def generate_id(self):
        """Generate unique ID untuk primary key"""
        return str(uuid.uuid4())

    def get_user(self, username):
        """Ambil data user berdasarkan username"""
        df = self.load_sheet('users')
        user = df[df['username'] == username]
        return user.iloc[0] if not user.empty else None

    def create_report(self, report_data):
        """Buat laporan baru"""
        df = self.load_sheet('reports')
        report_data['report_id'] = self.generate_id()
        report_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_data['updated_at'] = report_data['created_at']
        report_data['status'] = 'pending'
        
        df = pd.concat([df, pd.DataFrame([report_data])], ignore_index=True)
        self.save_sheet(df, 'reports')
        return report_data['report_id']

    def update_report(self, report_id, update_data):
        """Update laporan yang sudah ada"""
        df = self.load_sheet('reports')
        mask = df['report_id'] == report_id
        if mask.any():
            update_data['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for key, value in update_data.items():
                df.loc[mask, key] = value
            self.save_sheet(df, 'reports')
            return True
        return False

    def create_validation(self, validation_data):
        """Buat validasi baru"""
        df = self.load_sheet('validations')
        validation_data['validation_id'] = self.generate_id()
        validation_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        validation_data['updated_at'] = validation_data['created_at']
        
        df = pd.concat([df, pd.DataFrame([validation_data])], ignore_index=True)
        self.save_sheet(df, 'validations')
        return validation_data['validation_id']

    def create_revision(self, revision_data):
        """Buat revisi baru"""
        df = self.load_sheet('revision_history')
        revision_data['revision_id'] = self.generate_id()
        revision_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        df = pd.concat([df, pd.DataFrame([revision_data])], ignore_index=True)
        self.save_sheet(df, 'revision_history')
        return revision_data['revision_id']

    def get_report(self, report_id):
        """Ambil laporan berdasarkan ID"""
        df = self.load_sheet('reports')
        report = df[df['report_id'] == report_id]
        return report.iloc[0] if not report.empty else None

    def get_user_reports(self, username):
        """Ambil semua laporan user"""
        df = self.load_sheet('reports')
        return df[df['reporter_username'] == username]

    def get_pending_reports(self):
        """Ambil semua laporan yang pending"""
        df = self.load_sheet('reports')
        return df[df['status'] == 'pending']

    def get_validator_history(self, validator_username):
        """Ambil history validasi dari validator"""
        df = self.load_sheet('validations')
        return df[df['validator_username'] == validator_username]

    def get_report_validations(self, report_id):
        """Ambil semua validasi untuk suatu laporan"""
        df = self.load_sheet('validations')
        return df[df['report_id'] == report_id]

    def get_report_revisions(self, report_id):
        """Ambil history revisi untuk suatu laporan"""
        df = self.load_sheet('revision_history')
        return df[df['report_id'] == report_id]