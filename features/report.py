import os
import pandas as pd
from pathlib import Path

class CekLaporan:
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
        except Exception as e:
            print(f"Error loading the file: {e}")
            return pd.DataFrame(columns=[
                'report_id', 'journal_name', 'journal_url', 'reason',
                'is_anonymous', 'reporter_username', 'status',
                'created_at', 'updated_at'
            ])

    def display_reports(self, reports):
        """Display list laporan."""
        if reports.empty:
            print("\nTidak ada laporan yang ditemukan.")
            return

        print("\n=== Cek Laporan Jurnal Predator ===")
        print(f"{'ID Laporan':<12}{'Nama Jurnal':<30}{'URL Jurnal':<50}{'Alasan':<50}{'Status':<10}{'Reporter':<15}")
        print("="*175)

        #looping pada seluruh data dan menampilkan ID laporan
        for index, row in reports.iterrows():
            report_id = row['report_id']
            journal_name = row['journal_name']
            journal_url = row['journal_url']
            reason = row['reason']
            status = row['status']
            reporter = row['reporter_username'] if not row['is_anonymous'] else "Anonym"

            print(f"{report_id:<12}{journal_name:<30}{journal_url:<50}{reason:<50}{status:<10}{reporter:<15}")

    def show_report_details(self, report):
        """Display detail dari laporan."""
        report_id = report['report_id']
        journal_name = report['journal_name']
        journal_url = report['journal_url']
        reason = report['reason']
        status = report['status']
        reporter = report['reporter_username'] if not report['is_anonymous'] else "Anonym"
        created_at = report['created_at']
        updated_at = report['updated_at']
        
        print("\n=== Detail Laporan Jurnal Predator ===")
        print(f"ID Laporan          : {report_id}")
        print(f"Nama Jurnal         : {journal_name}")
        print(f"URL Jurnal          : {journal_url}")
        print(f"Alasan              : {reason}")
        print(f"Status              : {status}")
        print(f"Reporter            : {reporter}")
        print(f"Tanggal Dibuat      : {created_at}")
        print(f'Tanggal Diperbarui  : {updated_at}')
        print("="*100)
        
        input("\nTekan Enter untuk kembali ke menu...")

    def cek_laporan(self):
        """Menampilkan data laporan yang ada di database dan memungkinkan memilih laporan untuk detailnya."""
        reports = self.load_reports()  #load laporan
        self.display_reports(reports)  #list laporan

        while True:
            #user menginput id laporan untuk detailnya (ID format: RPT001, RPT002, ...)
            report_id = input("\nMasukkan ID laporan yang ingin dilihat detailnya (0 untuk kembali): ").strip().upper()

            if report_id == '0':
                print("\nKembali ke menu...")
                return

            #mencari report_id yang true pada row 'report_id'
            selected_report = reports[reports['report_id'] == report_id]

            #jika tidak ditemukan true
            if selected_report.empty:
                print("\nID laporan tidak ditemukan. Silakan coba lagi.")
            else:
                #tampilkan detail dari laporan
                self.show_report_details(selected_report.iloc[0]) #iloc untuk mengakses dari indeks 0
                break 