import pandas as pd
from datetime import datetime
from tabulate import tabulate

class ReportController:
    def __init__(self, report_file):
        self.report_file = report_file

    def report_journal(self, user_id, full_name):
        """Fitur melaporkan jurnal."""
        print("\n=== Report Journal ===")

        # Input apakah ingin melapor sebagai anonim
        while True:
            is_anonymous_input = input("Do you want to report as anonymous? (Y/N): ").strip().lower()
            if is_anonymous_input == "y":
                is_anonymous = True
                reporter_name = "Anonymous"
                break
            elif is_anonymous_input == "n":
                is_anonymous = False
                reporter_name = full_name
                break
            else:
                print("Invalid choice. Please enter Y or N.")

        # Input nama jurnal
        journal_name = input("Enter journal name: ").strip()

        # Input URL jurnal
        while True:
            journal_url = input("Enter journal URL: ").strip()
            if journal_url.startswith("http"):
                break
            else:
                print("Invalid URL. Please enter a valid URL starting with 'http'.")

        # Input alasan laporan
        reason = input("Enter your reason for reporting: ").strip()

        # Baca file CSV
        try:
            report_data = pd.read_csv(self.report_file)
        except FileNotFoundError:
            # Buat file baru jika belum ada
            report_data = pd.DataFrame(columns=[
                "report_id", "user_id", "full_name", "is_anonymous", "journal_name",
                "journal_url", "reason", "status_laporan", "tanggal_laporan"
            ])

        # Buat report_id baru
        report_id = int(report_data["report_id"].max() + 1) if not report_data.empty else 1

        # Tambahkan laporan baru
        new_report = {
            "report_id": report_id,
            "user_id": user_id,
            "full_name": reporter_name,
            "is_anonymous": is_anonymous,
            "journal_name": journal_name,
            "journal_url": journal_url,
            "reason": reason,
            "status_laporan": "pending",
            "tanggal_laporan": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        report_data = pd.concat([report_data, pd.DataFrame([new_report])], ignore_index=True)

        # Simpan kembali ke file CSV
        report_data.to_csv(self.report_file, index=False)

        # Tampilkan laporan tanpa kolom is_anonymous
        print("\nReport submitted successfully!")
        print("\n=== Submitted Report ===")
        display_report = {key: value for key, value in new_report.items() if key != "is_anonymous"}  # Exclude is_anonymous
        print(tabulate([display_report.values()], headers=display_report.keys(), tablefmt="grid"))
        
    def track_reports(self, user_id):
        """Fitur untuk user melihat laporan mereka."""
        print("\n=== Tracking Reports ===")

        try:
            # Baca data laporan dari file CSV
            report_data = pd.read_csv(self.report_file)

            # Filter laporan berdasarkan user_id
            user_reports = report_data[report_data["user_id"] == user_id]

            if user_reports.empty:
                print("You have not submitted any reports yet.")
            else:
                # Tampilkan laporan dalam bentuk tabel
                print("\nYour Reports:")
                display_data = user_reports[[
                    "report_id", "journal_name", "journal_url", "reason",
                    "status_laporan", "tanggal_laporan"
                ]]
                from tabulate import tabulate
                print(tabulate(display_data, headers="keys", tablefmt="grid"))
        except FileNotFoundError:
            print("No report data found. Please submit a report first.")
