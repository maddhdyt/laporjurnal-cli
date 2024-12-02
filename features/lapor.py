import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

class LaporJurnal:
    def __init__(self):
        self.file_path = Path('db/db_file.xlsx')
        os.makedirs(self.file_path.parent, exist_ok=True)
    
    def load_reports(self):
        """Load data laporan dari Excel"""
        if not os.path.exists(self.file_path):
            return pd.DataFrame(columns=[
                'report_id', 'journal_name', 'journal_url', 'reason',
                'is_anonymous', 'reporter_username', 'status',
                'created_at', 'updated_at'
            ])
        try:
            return pd.read_excel(self.file_path, sheet_name='reports')
        except:
            return pd.DataFrame(columns=[
                'report_id', 'journal_name', 'journal_url', 'reason',
                'is_anonymous', 'reporter_username', 'status',
                'created_at', 'updated_at'
            ])
    
    def save_reports(self, df):
        """Simpan data laporan ke Excel"""
        if not os.path.exists(self.file_path):
            df.to_excel(self.file_path, sheet_name='reports', index=False)
        else:
            with pd.ExcelWriter(self.file_path, mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='reports', index=False)
    
    def generate_report_id(self):
        """Generate ID laporan baru"""
        reports = self.load_reports()
        if reports.empty:
            return "RPT001"
        last_id = reports['report_id'].iloc[-1]
        num = int(last_id[3:]) + 1
        return f"RPT{num:03d}"
    
    def lapor_jurnal(self, current_user):
        """Proses pelaporan jurnal predator"""
        print("\n=== Lapor Jurnal Predator ===")
        
        # Input data laporan
        journal_name = input("Nama Jurnal: ").strip()
        journal_url = input("URL Jurnal: ").strip()
        reason = input("Alasan Pelaporan: ").strip()
        
        # Pilihan untuk laporan anonim
        while True:
            is_anonymous = input("Laporkan sebagai anonim? (y/n): ").strip().lower()
            if is_anonymous in ['y', 'n']:
                break
            print("Pilihan tidak valid!")
        
        # Buat data laporan baru
        report_data = {
            'report_id': self.generate_report_id(),
            'journal_name': journal_name,
            'journal_url': journal_url,
            'reason': reason,
            'is_anonymous': is_anonymous == 'y',
            'reporter_username': None if is_anonymous == 'y' else current_user['username'],
            'status': 'pending',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            # Load data yang ada
            reports_df = self.load_reports()
            
            # Tambahkan laporan baru
            reports_df = pd.concat([reports_df, pd.DataFrame([report_data])], ignore_index=True)
            
            # Simpan ke file
            self.save_reports(reports_df)
            
            print("\nLaporan berhasil disimpan!")
            print(f"ID Laporan: {report_data['report_id']}")
            input("\nTekan Enter untuk kembali ke menu...")
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("\nTekan Enter untuk kembali ke menu...")