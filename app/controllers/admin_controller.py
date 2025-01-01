import pandas as pd
from app.models.user_model import CSVModel
from app.controllers.auth_controller import AuthController
from tabulate import tabulate

class AdminController:
    def __init__(self):
        self.report_model = CSVModel("database/tb_report.csv")
        self.user_model = CSVModel("database/tb_user.csv")
        self.validator_model = CSVModel("database/tb_validator.csv")
        self.auth_controller = AuthController()

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
        """Menampilkan detail laporan sesuai template yang diminta."""
        try:
            # Baca data laporan
            report_data = self.report_model.read_data()
            report = report_data[report_data["report_id"] == report_id]
    
            if report.empty:
                print("Report not found.")
                return
    
            # Ambil informasi laporan
            report = report.iloc[0]  # Ambil baris pertama
    
            # Baca data user untuk mendapatkan nama dan instansi pelapor
            user_data = self.user_model.read_data()
            user = user_data[user_data["user_id"] == report["user_id"]]
    
            # Baca data validator untuk mendapatkan nama, instansi, dan profile validator
            validator_data = self.validator_model.read_data()
            validator = validator_data[validator_data["validator_id"] == report["validator_id"]]
    
            # Tampilkan detail laporan
            print("\n=== Report Details ===")
            print(f"Report ID: {report['report_id']}")
            print(f"Date Submitted: {report['tanggal_laporan']}")
            print(f"Journal Name: {report['journal_name']}")
            print(f"Journal URL: {report['journal_url']}")
            print(f"Nama Pelapor: {user.iloc[0]['full_name'] if not user.empty else 'N/A'}")
            print(f"Instansi Pelapor: {user.iloc[0]['instancy'] if not user.empty else 'N/A'}")
            print(f"Reason: {report['reason']}")
    
            # Tampilkan hasil review (jika ada)
            print("\n=== Review Result ===")
            if not validator.empty:
                validator = validator.iloc[0]  # Ambil baris pertama
                print(f"Nama Validator: {validator['full_name']}")
                print(f"Instansi Validator: {validator['instancy']}")
                print("Profile Validator:")
                if pd.notna(validator['scopus_url']):
                    print(f"- {validator['scopus_url']}")
                if pd.notna(validator['sinta_url']):
                    print(f"- {validator['sinta_url']}")
                if pd.notna(validator['google_scholar_url']):
                    print(f"- {validator['google_scholar_url']}")
            else:
                print("Nama Validator: N/A")
                print("Instansi Validator: N/A")
                print("Profile Validator: N/A")
    
            print(f"Status Laporan: {report['status_laporan']}")
            print(f"Status Jurnal: {report['status_jurnal'] if not pd.isna(report['status_jurnal']) else 'N/A'}")
            print(f"Feedback: {report['feedback'] if not pd.isna(report['feedback']) else 'N/A'}")
        except Exception as e:
            print(f"Error: {e}")

    def view_all_users(self):
        """Menampilkan semua akun user dan memberikan opsi untuk menghapus."""
        print("\n=== All Users ===")
        try:
            user_data = self.user_model.read_data()
            if user_data.empty:
                print("No users found.")
            else:
                display_data = user_data[["user_id", "username", "instancy"]]
                print(tabulate(display_data, headers="keys", tablefmt="fancy_grid"))

                # Meminta admin untuk memasukkan user_id untuk melihat detail atau menghapus
                user_id = input("\nEnter User ID to view details, delete, or 0 to return: ").strip()
                if user_id == "0":
                    return

                try:
                    user_id = int(user_id)
                except ValueError:
                    print("Invalid User ID. Please enter a valid number.")
                    return

                # Cek apakah user_id ada dalam data
                if user_id in user_data["user_id"].values:
                    # Tampilkan detail pengguna
                    self.view_user_details(user_id)
                else:
                    print("User  ID not found.")
        except Exception as e:
            print(f"Error: {e}")

    def view_user_details(self, user_id):
        """Menampilkan detail pengguna dan memberikan opsi untuk menghapus."""
        try:
            user_data = self.user_model.read_data()
            user = user_data[user_data["user_id"] == user_id]

            if user.empty:
                print("User  not found.")
                return

            # Ambil informasi pengguna
            user = user.iloc[0]  # Ambil baris pertama
            print("\n=== User Details ===")
            print(f"User  ID: {user['user_id']}")
            print(f"Username: {user['username']}")
            print(f"Full Name: {user['full_name']}")
            print(f"Email: {user['email']}")
            print(f"Password: {user['password']}")
            print(f"Instancy: {user['instancy']}")
            print(f"Role: {user['role']}")

            # Opsi untuk menghapus pengguna
            choice = input("\nDo you want to delete this user? (Y/N): ").strip().lower()
            if choice == "y":
                self.delete_user(user_id)
            else:
                print("Operation canceled.")
        except Exception as e:
            print(f"Error: {e}")

    def delete_user(self, user_id):
        """Menghapus akun pengguna berdasarkan User ID."""
        try:
            # Konfirmasi penghapusan
            confirm = input("Are you sure you want to delete this user? (Y/N): ").strip().lower()
            if confirm != "y":
                print("Operation canceled.")
                return
    
            # Panggil metode delete_data dari user_model
            self.user_model.delete_data(user_id)
        except Exception as e:
            print(f"Error: {e}")

    def view_all_validators(self):
        """Menampilkan semua akun validator dan memberikan opsi untuk menghapus."""
        print("\n=== All Validators ===")
        try:
            validator_data = self.validator_model.read_data()
            if validator_data.empty:
                print("No validators found.")
            else:
                # Tampilkan hanya kolom validator_id, full_name, dan instancy
                display_data = validator_data[["validator_id", "full_name", "instancy"]]
                print(tabulate(display_data, headers="keys", tablefmt="fancy_grid"))

                # Meminta admin untuk memasukkan validator_id untuk melihat detail atau menghapus
                validator_id = input("\nEnter Validator ID to view details, delete, or 0 to return: ").strip()
                if validator_id == "0":
                    return

                try:
                    validator_id = int(validator_id)
                except ValueError:
                    print("Invalid Validator ID. Please enter a valid number.")
                    return

                # Cek apakah validator_id ada dalam data
                if validator_id in validator_data["validator_id"].values:
                    # Tampilkan detail validator
                    self.view_validator_details(validator_id)
                else:
                    print("Validator ID not found.")
        except Exception as e:
            print(f"Error: {e}")

    def view_validator_details(self, validator_id):
        """Menampilkan detail validator dan memberikan opsi untuk mengedit atau menghapus."""
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

            # Opsi untuk mengedit atau menghapus validator
            print("\nOptions:")
            print("1. Edit Validator")
            print("2. Delete Validator")
            print("3. Return to Validator List")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.edit_validator(validator_id)  # Panggil metode edit_validator
                
            elif choice == "2":
                self.delete_validator(validator_id)  # Panggil metode delete_validator
                
            elif choice == "3":
                return
            else:
                print("Invalid choice. Please try again.")
                input("\nPress Enter to continue...")
        except Exception as e:
            print(f"Error: {e}")
            
    def edit_validator(self, validator_id):
        """Mengedit data validator berdasarkan Validator ID."""
        try:
            # Baca data validator dari file CSV
            validator_data = self.validator_model.read_data()
            validator = validator_data[validator_data["validator_id"] == validator_id]

            if validator.empty:
                print("Validator not found.")
                return

            # Ambil informasi validator
            validator = validator.iloc[0]  # Ambil baris pertama
            print("\n=== Edit Validator ===")
            print(f"Validator ID: {validator['validator_id']} (Cannot be changed)")

            # Input untuk mengedit data
            while True:
                new_username = input(f"Enter new username (current: {validator['username']}): ").strip()
                if new_username:
                    if not self.auth_controller.is_valid_username(new_username):
                        print("Invalid username. Username must be at least 8 characters and can only contain letters, numbers, '_', and '.'.")
                        continue
                    if new_username != validator["username"] and new_username in validator_data["username"].values:
                        print("Username already exists. Please choose another one.")
                        continue
                break

            new_full_name = input(f"Enter new full name (current: {validator['full_name']}): ").strip()

            while True:
                new_email = input(f"Enter new email (current: {validator['email']}): ").strip()
                if new_email:
                    if not self.auth_controller.is_valid_email(new_email):
                        print("Invalid email format. Please try again.")
                        continue
                break

            while True:
                new_password = input(f"Enter new password (current: {validator['password']}): ").strip()
                if new_password:
                    if not self.auth_controller.is_valid_password(new_password):
                        print("Password must be at least 8 characters.")
                        continue
                break

            new_instancy = input(f"Enter new instancy (current: {validator['instancy']}): ").strip()

            new_academic_position = input(f"Enter new academic position (current: {validator['academic_position']}): ").strip()

            while True:
                new_scopus_url = input(f"Enter new Scopus URL (current: {validator['scopus_url']}): ").strip()
                if new_scopus_url and not new_scopus_url.startswith("http"):
                    print("Invalid Scopus URL. Please enter a valid URL starting with 'http'.")
                    continue
                break

            while True:
                new_sinta_url = input(f"Enter new Sinta URL (current: {validator['sinta_url']}): ").strip()
                if new_sinta_url and not new_sinta_url.startswith("http"):
                    print("Invalid Sinta URL. Please enter a valid URL starting with 'http'.")
                    continue
                break

            while True:
                new_google_scholar_url = input(f"Enter new Google Scholar URL (current: {validator['google_scholar_url']}): ").strip()
                if new_google_scholar_url and not new_google_scholar_url.startswith("http"):
                    print("Invalid Google Scholar URL. Please enter a valid URL starting with 'http'.")
                    continue
                break



            # Update data validator
            validator_data.loc[validator_data["validator_id"] == validator_id, "username"] = new_username or validator["username"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "full_name"] = new_full_name or validator["full_name"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "email"] = new_email or validator["email"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "password"] = new_password or validator["password"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "instancy"] = new_instancy or validator["instancy"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "academic_position"] = new_academic_position or validator["academic_position"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "scopus_url"] = new_scopus_url or validator["scopus_url"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "sinta_url"] = new_sinta_url or validator["sinta_url"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "google_scholar_url"] = new_google_scholar_url or validator["google_scholar_url"]

            # Simpan kembali ke file CSV
            self.validator_model.write_data(validator_data)
            print("Validator updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def delete_validator(self, validator_id):
        """Menghapus akun validator berdasarkan Validator ID."""
        try:
            # Konfirmasi penghapusan
            confirm = input("Are you sure you want to delete this validator? (Y/N): ").strip().lower()
            if confirm != "y":
                print("Operation canceled.")
                return

            # Panggil metode delete_validator dari AuthController
            self.auth_controller.delete_validator(validator_id)
        except Exception as e:
            print(f"Error: {e}")
            
    def view_statistics(self):
        """Menampilkan statistik/jumlah data."""
        try:
            # Baca data dari file CSV
            report_data = self.report_model.read_data()
            user_data = self.user_model.read_data()
            validator_data = self.validator_model.read_data()

            # Hitung statistik
            total_reports = len(report_data)  # Total Laporan
            total_users = len(user_data)  # Jumlah User
            total_validators = len(validator_data)  # Jumlah Validator
            pending_reports = len(report_data[report_data["status_laporan"] == "pending"])  # Laporan Pending
            review_reports = len(report_data[report_data["status_laporan"] == "review"])  # Laporan Review
            done_reports = len(report_data[report_data["status_laporan"] == "done"])  # Laporan Sukses

            # Tampilkan statistik dalam format yang rapi
            print("=== Statistics ===")
            print(f"Total Laporan: {total_reports}")
            print(f"Jumlah User: {total_users}")
            print(f"Jumlah Validator: {total_validators}")
            print(f"Laporan Pending: {pending_reports}")
            print(f"Laporan Review: {review_reports}")
            print(f"Laporan Sukses: {done_reports}")
        except Exception as e:
            print(f"Error: {e}")