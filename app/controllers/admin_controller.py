import pandas as pd
from app.models.user_model import CSVModel
from tabulate import tabulate


class AdminController:
    def __init__(self):
        self.report_model = CSVModel("database/tb_report.csv")
        self.user_model = CSVModel("database/tb_user.csv")
        self.validator_model = CSVModel("database/tb_validator.csv")

    def view_all_reports(self):
        """Menampilkan semua laporan yang ada."""
        print("\n=== All Reports ===")
        try:
            report_data = self.report_model.read_data()
            if report_data.empty:
                print("No reports found.")
            else:
                # Tampilkan ringkasan laporan
                display_data = report_data[["report_id", "journal_name", "journal_url", "status_laporan"]]
                print(tabulate(display_data, headers="keys", tablefmt="fancy_grid"))

                # Meminta pengguna untuk memasukkan report_id untuk melihat detail
                report_id = input("\nEnter Report ID to view details or 0 to return: ").strip()
                if report_id == "0":
                    return

                try:
                    report_id = int(report_id)
                except ValueError:
                    print("Invalid Report ID. Please try again.")
                    return

                # Menampilkan detail laporan berdasarkan report_id
                self.view_report_details(report_id)

        except Exception as e:
            print(f"Error: {e}")

    def view_report_details(self, report_id):
        """Menampilkan detail laporan berdasarkan Report ID."""
        try:
            report_data = self.report_model.read_data()
            report = report_data[report_data["report_id"] == report_id]

            if report.empty:
                print("Report not found.")
                return

            # Ambil informasi laporan
            report = report.iloc[0]  # Ambil baris pertama
            print("\n=== Report Details ===")
            print(f"Report ID: {report['report_id']}")
            print(f"Journal Name: {report['journal_name']}")
            print(f"Journal URL: {report['journal_url']}")
            print(f"Reason: {report['reason']}")
            print(f"Status Laporan: {report['status_laporan']}")
            print(f"Date Submitted: {report['tanggal_laporan']}")
            print(f"Feedback: {report['feedback'] if not pd.isna(report['feedback']) else 'N/A'}")
            print(f"Validator ID: {report['validator_id'] if not pd.isna(report['validator_id']) else 'N/A'}")

        except Exception as e:
            print(f"Error: {e}")

    def view_all_users(self):
        """Menampilkan semua akun user."""
        print("\n=== All Users ===")
        try:
            user_data = self.user_model.read_data()
            if user_data.empty:
                print("No users found.")
            else:
                # Menggunakan tabulate untuk menampilkan tabel dengan format yang lebih rapi
                print(tabulate(user_data, headers="keys", tablefmt="fancy_grid"))
        except Exception as e:
            print(f"Error: {e}")

    def view_all_validators(self):
        """Menampilkan semua akun validator."""
        print("\n=== All Validators ===")
        try:
            validator_data = self.validator_model.read_data()
            if validator_data.empty:
                print("No validators found.")
            else:
                # Menggunakan tabulate untuk menampilkan tabel dengan format yang lebih rapi
                print(tabulate(validator_data, headers="keys", tablefmt="fancy_grid"))
        except Exception as e:
            print(f"Error: {e}")