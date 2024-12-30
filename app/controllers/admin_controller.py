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
                # Tampilkan ringkasan validator
                display_data = validator_data[["validator_id", "username", "instancy", "academic_position"]]
                print(tabulate(display_data, headers="keys", tablefmt="fancy_grid"))

                # Meminta pengguna untuk memasukkan validator_id untuk melihat detail
                validator_id = input("\nEnter Validator ID to view details or 0 to return: ").strip()
                if validator_id == "0":
                    return

                try:
                    validator_id = int(validator_id)
                except ValueError:
                    print("Invalid Validator ID. Please try again.")
                    return

                # Menampilkan detail validator berdasarkan validator_id
                self.view_validator_details(validator_id)

        except Exception as e:
            print(f"Error: {e}")

    def view_validator_details(self, validator_id):
        """Menampilkan detail validator berdasarkan Validator ID."""
        try:
            validator_data = self.validator_model.read_data()
            validator = validator_data[validator_data["validator_id"] == validator_id]

            if validator.empty:
                print("Validator not found.")
                return

            # Ambil informasi validator
            validator = validator.iloc[0]  # Ambil baris pertama
            print("\n=== Validator Details ===")
            print(f"Validator ID: {validator['validator_id']}")
            print(f"Username: {validator['username']}")
            print(f"Full Name: {validator['full_name']}")
            print(f"Email: {validator['email']}")
            print(f"Instancy: {validator['instancy']}")
            print(f"Academic Position: {validator['academic_position']}")
            print(f"Scopus URL: {validator['scopus_url']}")
            print(f"Sinta URL: {validator['sinta_url']}")
            print(f"Google Scholar URL: {validator['google_scholar_url']}")
            print(f"Role: {validator['role']}")

        except Exception as e:
            print(f"Error: {e}")