import os
import pandas as pd
from pathlib import Path

class ValidasiLaporan:
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
        """Display list laporan dengan semua informasi"""
        if reports.empty:
            print("\nTidak ada laporan yang ditemukan.")
            return
        
        print(f"{'ID Laporan':<12}{'Nama Jurnal':<30}{'URL Jurnal':<50}{'Status':<10}{'Reporter':<15}{'Updated_at':<20}")
        print("="*150)

        # Looping pada seluruh data
        for index, row in reports.iterrows():
            report_id = row['report_id']
            journal_name = row['journal_name']
            journal_url = row['journal_url']
            status = row['status']
            reporter = row['reporter_username'] if not row['is_anonymous'] else "Anonym"
            updated_at = row['updated_at']

            print(f"{report_id:<12}{journal_name:<30}{journal_url:<50}{status:<10}{reporter:<15}{updated_at:<20}")

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

    def save_reports(self, df):
        """Simpan data laporan yang sudah diperbarui ke Excel"""
        with pd.ExcelWriter(self.file_path, mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='reports', index=False)

    def validate_report(self, reports):
        """Memvalidasi laporan jurnal predator dengan menampilkan data lengkap"""
        if reports.empty:
            print("Tidak ada laporan yang tersedia untuk diedit.")
            return
        
        print("\n=== Validasi Laporan ===")
        # Menampilkan laporan secara lengkap
        self.display_reports(reports)
        
        # Pilih laporan untuk diedit
        report_id = input("\nMasukkan ID laporan yang ingin divalidasi (misal: RPT001): ").strip().upper()
        
        # Cek apakah laporan dengan ID tersebut ada
        report = reports[reports['report_id'] == report_id]
        if report.empty:
            print("ID laporan tidak ditemukan!")
            return
        
        # Menampilkan detail laporan
        self.show_report_details(report.iloc[0])
        
        # Pilihan status
        while True:
            status = input("Masukkan status baru (Done/Rejected): ").strip().lower()
            if status in ['done', 'rejected']:
                break
            print("Pilihan tidak valid! Status harus 'Done' atau 'Rejected'.")
        
        # Update status laporan
        reports.loc[reports['report_id'] == report_id, 'status'] = status.capitalize()
        reports.loc[reports['report_id'] == report_id, 'updated_at'] = pd.to_datetime('now').strftime("%Y-%m-%d %H:%M:%S")
        
        # Simpan perubahan
        self.save_reports(reports)
        
        print(f"\nStatus laporan ID {report_id} berhasil diubah menjadi '{status.capitalize()}'.")
        input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    validasi_laporan = ValidasiLaporan()
    reports_df = validasi_laporan.load_reports()
    validasi_laporan.validate_report(reports_df)
