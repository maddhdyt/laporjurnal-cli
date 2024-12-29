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
                print(tabulate(report_data, headers="keys", tablefmt="grid"))
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
                print(tabulate(user_data, headers="keys", tablefmt="grid"))
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
                print(tabulate(validator_data, headers="keys", tablefmt="grid"))
        except Exception as e:
            print(f"Error: {e}")

    def admin_menu(self):
        """Menu untuk admin."""
        while True:
            print("\n=== Admin Menu ===")
            print("1. View All Reports")
            print("2. View All Users")
            print("3. View All Validators")
            print("4. Logout")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.view_all_reports()
                input("\nPress Enter to return to the admin menu...")
            elif choice == "2":
                self.view_all_users()
                input("\nPress Enter to return to the admin menu...")
            elif choice == "3":
                self.view_all_validators()
                input("\nPress Enter to return to the admin menu...")
            elif choice == "4":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")