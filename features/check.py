import os
import pandas as pd
from pathlib import Path

class CekJurnal:
    def __init__(self):
        self.file_path = Path('db/db_file.xlsx')

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
    
    def show_report_details(self, report):
        """Display detail dari laporan."""
        report_id = report['report_id']
        journal_name = report['journal_name']
        journal_url = report['journal_url']
        reason = report['reason']
        status = report['status']
        reporter = report['reporter_username'] if not report['is_anonymous'] else "Anonym"
        created_at = report['created_at']

        print("\n=== Detail Laporan Jurnal Predator ===")
        print(f"ID Laporan     : {report_id}")
        print(f"Nama Jurnal    : {journal_name}")
        print(f"URL Jurnal     : {journal_url}")
        print(f"Alasan         : {reason}")
        print(f"Status         : {status}")
        print(f"Reporter       : {reporter}")
        print(f"Tanggal Dibuat : {created_at}")
        print("="*100)
        
        input("\nTekan Enter untuk kembali ke menu...")

    def cek_jurnal(self):
        """Memeriksa apakah jurnal sudah terdaftar sebagai predator berdasarkan URL"""
        reports_df = self.load_reports()
        journal_url = input("URL jurnal yang ingin dicek: ")

        #cek kesamaan url dengan database yang sudah ada (case-sensitive)
        matched_reports = reports_df[reports_df['journal_url'] == journal_url]

        if not matched_reports.empty:
            self.show_report_details(matched_reports.iloc[0])
        else:
            print("\nJurnal ini tidak terdaftar sebagai jurnal predator.")
        
        input("Fitur masih dalam tahap pengembangan.")
