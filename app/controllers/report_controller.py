import pandas as pd
from datetime import datetime

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
            # Jika file tidak ada, buat DataFrame baru dengan kolom yang sesuai
            report_data = pd.DataFrame(columns=[
                "report_id", "user_id", "is_anonymous", "journal_url", "journal_name",
                "reason", "status_laporan", "status_jurnal", "feedback", "validator_id", "tanggal_laporan"
            ])

        # Tambahkan laporan baru
        new_report = pd.DataFrame([{
            "report_id": report_id,
            "user_id": user_id,           # Tetap menyimpan user_id
            "is_anonymous": is_anonymous, # Simpan status anonim
            "journal_url": journal_url,
            "journal_name": journal_name,
            "reason": reason,
            "status_laporan": "pending",  # Status laporan default
            "status_jurnal": None,        # Status jurnal default kosong
            "feedback": None,             # Feedback kosong saat laporan dibuat
            "validator_id": None,         # Validator belum ditugaskan
            "tanggal_laporan": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Tambahkan tanggal laporan
        }])

        # Pastikan kolom DataFrame tidak kosong sebelum concatenation
        if report_data.empty:
            report_data = new_report
        else:
            report_data = pd.concat([report_data, new_report], ignore_index=True)

        # Simpan data ke Excel
        report_data.to_excel(self.report_file, index=False, engine="openpyxl")
        print(f"Laporan berhasil dibuat dengan ID: {report_id}")

    def list_pending_reports(self, validator_id):
        """Menampilkan daftar laporan pending."""
        print("\n=== Pending Reports ===")
        try:
            report_data = pd.read_excel(self.report_file, engine="openpyxl")
            # Filter laporan dengan status pending
            pending_reports = report_data[report_data["status_laporan"] == "pending"].copy()

            if pending_reports.empty:
                print("No pending reports found.")
                return

            # Tampilkan laporan pending
            display_data = pending_reports[["report_id", "tanggal_laporan", "user_id", "journal_name", "journal_url"]]
            print(display_data.to_string(index=False))

            # Submenu untuk pending reports
            while True:
                print("\nOptions:")
                print("1. Accept a report for review")
                print("2. Back to menu")
                choice = input("Choose an option: ")

                if choice == "1":
                    self.accept_report(validator_id)  # Panggil fungsi accept_report
                    break
                elif choice == "2":
                    return
                else:
                    print("Invalid choice. Please try again.")
        except FileNotFoundError:
            print("No reports database found.")

    def list_accepted_reports(self, validator_id):
        """Menampilkan daftar laporan yang diterima validator."""
        print("\n=== Accepted Reports ===")
        try:
            # Baca data dari file laporan
            report_data = pd.read_excel(self.report_file, engine="openpyxl")

            # Debugging: Tampilkan semua data sebelum difilter
            print("\nFull Report Data:")
            print(report_data)

            # Filter laporan dengan status review dan diterima oleh validator yang login
            accepted_reports = report_data[
                (report_data["status_laporan"] == "review") &
                (report_data["validator_id"].notna()) &  # Pastikan validator_id bukan NaN
                (report_data["validator_id"] == float(validator_id))  # Bandingkan dengan float
            ].copy()

            # Debugging: Tampilkan data setelah difilter
            print("\nFiltered Accepted Reports:")
            print(accepted_reports)

            if accepted_reports.empty:
                print("No accepted reports found.")
                return

            # Tampilkan laporan diterima
            display_data = accepted_reports[["report_id", "tanggal_laporan", "journal_name", "journal_url", "reason"]]
            print(display_data.to_string(index=False))
        except FileNotFoundError:
            print("No reports database found.")



    def view_report_details(self, report_data):
        """Menampilkan detail laporan berdasarkan ID."""
        try:
            report_id = int(input("Enter Report ID to view details: "))
            report = report_data[report_data["report_id"] == report_id]

            if report.empty:
                print("No report found with the given ID.")
            else:
                for col in report.columns:
                    print(f"{col}: {report.iloc[0][col]}")
        except ValueError:
            print("Invalid input. Please enter a valid Report ID.")
            
    def review_report(self, validator_id):
        """Melakukan review laporan."""
        print("\n=== Review Report ===")
        try:
            report_data = pd.read_excel(self.report_file, engine="openpyxl")
            # Filter laporan yang diterima oleh validator
            accepted_reports = report_data[
                (report_data["status_laporan"] == "review") & (report_data["validator_id"] == validator_id)
            ]

            if accepted_reports.empty:
                print("No reports available for review.")
                return

            # Pilih laporan untuk review
            print("\nAccepted Reports:")
            display_data = accepted_reports[["report_id", "journal_name", "journal_url", "reason"]]
            print(display_data.to_string(index=False))

            report_id = int(input("Enter Report ID to review: "))
            if report_id not in accepted_reports["report_id"].values:
                print("Invalid Report ID.")
                return

            # Validasi laporan
            print("\nOptions for journal status:")
            print("1. Aman")
            print("2. Predator")
            print("3. Clone")
            status_choice = input("Choose journal status: ")

            status_jurnal = {"1": "aman", "2": "predator", "3": "clone"}.get(status_choice)
            if not status_jurnal:
                print("Invalid choice.")
                return

            decision = input("Enter report status (Done/Rejected): ").strip().lower()
            if decision not in ["done", "rejected"]:
                print("Invalid status.")
                return

            feedback = input("Enter your feedback: ").strip()

            # Update laporan
            report_data.loc[report_data["report_id"] == report_id, "status_laporan"] = decision.capitalize()
            report_data.loc[report_data["report_id"] == report_id, "status_jurnal"] = status_jurnal
            report_data.loc[report_data["report_id"] == report_id, "feedback"] = feedback
            report_data.to_excel(self.report_file, index=False, engine="openpyxl")
            print(f"Report ID {report_id} has been reviewed successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid Report ID.")
        except FileNotFoundError:
            print("No reports database found.")
            
    def return_report_to_pending(self, report_data):
        """Mengembalikan laporan ke status pending."""
        print("\n=== Return Report to Pending ===")
        try:
            report_id = int(input("Enter Report ID to return: "))
            if report_id not in report_data["report_id"].values:
                print("Invalid Report ID.")
                return

            # Update status laporan menjadi pending
            report_data.loc[report_data["report_id"] == report_id, "status_laporan"] = "pending"
            report_data.loc[report_data["report_id"] == report_id, "validator_id"] = None
            report_data.to_excel(self.report_file, index=False, engine="openpyxl")
            print(f"Report ID {report_id} has been returned to pending.")
        except ValueError:
            print("Invalid input. Please enter a valid Report ID.")

    def accept_report(self, validator_id):
        """Menerima laporan untuk direview."""
        print("\n=== Accept Report ===")
        try:
            # Baca data laporan
            report_data = pd.read_excel(self.report_file, engine="openpyxl")

            # Inisialisasi kolom validator_id sebagai string jika belum ada atau semua nilainya NaN
            if "validator_id" not in report_data.columns:
                report_data["validator_id"] = None  # Kolom baru dengan nilai None
            else:
                report_data["validator_id"] = report_data["validator_id"].astype(str)  # Pastikan tipe string

            # Filter laporan dengan status pending
            pending_reports = report_data[report_data["status_laporan"] == "pending"].copy()

            if pending_reports.empty:
                print("No pending reports found.")
                return

            # Tampilkan laporan pending
            display_data = pending_reports[["report_id", "tanggal_laporan", "journal_name", "journal_url"]]
            print(display_data.to_string(index=False))

            # Pilih laporan untuk diterima
            report_id = int(input("\nEnter Report ID to accept: "))
            if report_id not in pending_reports["report_id"].values:
                print("Invalid Report ID.")
                return

            # Debugging: Tampilkan sebelum perubahan
            print("\nData Before Update:")
            print(report_data[report_data["report_id"] == report_id])

            # Ubah status laporan menjadi review dan simpan validator_id
            report_data.loc[report_data["report_id"] == report_id, "status_laporan"] = "review"
            report_data.loc[report_data["report_id"] == report_id, "validator_id"] = str(validator_id)  # Simpan sebagai string

            # Debugging: Tampilkan setelah perubahan
            print("\nData After Update:")
            print(report_data[report_data["report_id"] == report_id])

            # Simpan data kembali ke file Excel
            report_data.to_excel(self.report_file, index=False, engine="openpyxl")
            print(f"Report ID {report_id} has been accepted for review.")
        except ValueError as ve:
            print(f"Invalid input or conversion error: {ve}")
        except FileNotFoundError:
            print("No reports database found.")
























