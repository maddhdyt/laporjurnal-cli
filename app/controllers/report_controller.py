import pandas as pd

from app.views.report_view import show_list_of_reports

class ReportController:
    def __init__(self, report_file="database/tb_report.xlsx"):
        self.report_file = report_file

    def report_journal(self, user_id):
        """Fungsi untuk melaporkan jurnal."""
        print("\n=== Report Journal ===")

        # Input apakah ingin melapor sebagai anonim
        while True:
            is_anonymous_input = input("Do you want to report as anonymous? (Y/N): ").strip().lower()
            if is_anonymous_input == "y":
                is_anonymous = True
                break
            elif is_anonymous_input == "n":
                is_anonymous = False
                break
            else:
                print("Invalid choice. Please enter Y or N.")

        # Input URL jurnal
        journal_url = input("Enter journal URL: ").strip()

        # Input nama jurnal
        journal_name = input("Enter journal name: ").strip()

        # Input alasan laporan
        reason = input("Enter your reason for reporting: ").strip()

        # Siapkan data laporan
        report_id = 1
        try:
            report_data = pd.read_excel(self.report_file, engine="openpyxl")
            if not report_data.empty:
                report_id = report_data["report_id"].max() + 1
        except FileNotFoundError:
            # Jika file tidak ada, buat file baru
            report_data = pd.DataFrame(columns=[
                "report_id", "user_id", "is_anonymous", "journal_url", "journal_name",
                "reason", "status", "feedback", "validator_id"
            ])

        # Tambahkan laporan baru
        new_report = pd.DataFrame([{
            "report_id": report_id,
            "user_id": user_id,           # Tetap menyimpan user_id
            "is_anonymous": is_anonymous, # Simpan status anonim
            "journal_url": journal_url,
            "journal_name": journal_name,
            "reason": reason,
            "status": "Pending",          # Status awal
            "feedback": "",               # Feedback kosong saat laporan dibuat
            "validator_id": None          # Validator belum ditugaskan
        }])

        # Gunakan pd.concat untuk menambahkan data baru
        report_data = pd.concat([report_data, new_report], ignore_index=True)
        report_data.to_excel(self.report_file, index=False, engine="openpyxl")
        print(f"Laporan berhasil dibuat dengan ID: {report_id}")

    def list_reports(self, status="Pending"):
        """Menampilkan daftar laporan berdasarkan status."""
        try:
            report_data = pd.read_excel(self.report_file, engine="openpyxl")
            filtered_reports = report_data[report_data["status"] == status].copy()
            show_list_of_reports(filtered_reports, status)
        except FileNotFoundError:
            print("No reports database found. Please report a journal first.")





