import pandas as pd
from utils import clear_screen
from app.models.CSVModel import CSVModel
from app.controllers.auth_controller import AuthController
from tabulate import tabulate

class AdminController:
    def __init__(self):
        self.report_model = CSVModel("database/tb_report.csv")
        self.user_model = CSVModel("database/tb_user.csv")
        self.validator_model = CSVModel("database/tb_validator.csv")
        self.auth_controller = AuthController()
        
    def view_statistics(self):
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

    def view_all_reports(self):
        clear_screen()
        while True:
            print("\n=== All Reports ===")
            try:
                report_data = self.report_model.read_data()
                if report_data.empty:
                    print("No reports found.")
                    return  
                else:
                    display_data = report_data[["report_id", "journal_name", "journal_url", "status_laporan"]]
                    print(tabulate(display_data, headers="keys", tablefmt="fancy_grid"))

                    while True:
                        report_id = input("\nEnter Report ID to view details or 0 to return: ").strip()
                        if report_id == "0":
                            return
                        elif report_id.isdigit():
                            report_id = int(report_id)
                            if report_id in report_data["report_id"].values:
                                self.view_report_details(report_id)
                                break 
                            else:
                                print("Report ID not found. Please try again.")
                        else:
                            print("Invalid input. Please enter a valid Report ID or 0 to return.")
            except Exception as e:
                print(f"Error: {e}")

    def view_report_details(self, report_id):
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
            
            # Opsi untuk kembali ke daftar laporan
            while True:
                choice = input("\nPress 0 to return to the report list: ").strip()
                if choice == "0":
                    return  # Kembali ke daftar laporan
                else:
                    print("Invalid input. Please press 0 to return.")
        except Exception as e:
            print(f"Error: {e}")

    def view_all_users(self):
        clear_screen()
        print("\n=== All Users ===")
        try:
            user_data = self.user_model.read_data()
            if user_data.empty:
                print("No users found.")
                return  # Kembali ke menu sebelumnya jika tidak ada data user
            else:
                # Tampilkan hanya kolom user_id, full_name, dan instancy
                display_data = user_data[["user_id", "full_name", "instancy"]]
                print(tabulate(display_data, headers="keys", tablefmt="fancy_grid"))

                while True:
                    # Meminta admin untuk memasukkan user_id untuk melihat detail atau menghapus
                    user_id = input("\nEnter User ID to view details, delete, or 0 to return: ").strip()

                    # Validasi input: harus berupa angka
                    if not user_id.isdigit():
                        print("Invalid input. Please enter a valid User ID (number) or 0 to return.")
                        continue  # Lanjutkan loop untuk meminta input lagi

                    user_id = int(user_id)  # Konversi input ke integer

                    if user_id == 0:
                        return  # Kembali ke menu admin langsung
                    elif user_id in user_data["user_id"].values:
                        # Tampilkan detail pengguna
                        self.view_user_details(user_id)
                        break  # Keluar dari loop setelah kembali dari view_user_details
                    else:
                        print("User  ID not found. Please try again.")
        except Exception as e:
            print(f"Error: {e}")

    def view_user_details(self, user_id):
        clear_screen()
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

            # Loop untuk memastikan input yang valid
            while True:
                print("\nOptions:")
                print("1. Delete User")
                print("2. Return to User List")
                choice = input("Choose an option: ").strip()

                if choice == "1":
                    self.delete_user(user_id)
                    break  # Keluar dari loop setelah menghapus pengguna
                elif choice == "2":
                    # Tampilkan tabel pengguna lagi
                    self.view_all_users()
                    return  # Kembali ke menu admin setelah menampilkan tabel
                else:
                    print("Invalid choice. Please try again.")
                    # Loop akan berlanjut hingga input yang valid diberikan

        except Exception as e:
            print(f"Error: {e}")

    def view_all_validators(self):
        clear_screen()
        print("\n=== All Validators ===")
        try:
            validator_data = self.validator_model.read_data()
            if validator_data.empty:
                print("No validators found.")
                return  # Kembali ke menu sebelumnya jika tidak ada data validator
            else:
                # Tampilkan hanya kolom validator_id, full_name, dan instancy
                display_data = validator_data[["validator_id", "full_name", "instancy"]]
                print(tabulate(display_data, headers="keys", tablefmt="fancy_grid"))

                while True:
                    # Meminta admin untuk memasukkan validator_id untuk melihat detail atau menghapus
                    validator_id = input("\nEnter Validator ID to view details, delete, or 0 to return: ").strip()

                    # Validasi input: harus berupa angka
                    if not validator_id.isdigit():
                        print("Invalid input. Please enter a valid Validator ID (number) or 0 to return.")
                        continue  # Lanjutkan loop untuk meminta input lagi

                    validator_id = int(validator_id)  # Konversi input ke integer

                    if validator_id == 0:
                        return  # Kembali ke menu admin langsung
                    elif validator_id in validator_data["validator_id"].values:
                        # Tampilkan detail validator
                        self.view_validator_details(validator_id)
                        break  # Keluar dari loop setelah kembali dari view_validator_details
                    else:
                        print("Validator ID not found. Please try again.")
        except Exception as e:
            print(f"Error: {e}")

    def view_validator_details(self, validator_id):
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
            while True:
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
                    self.view_all_validators()  # Tampilkan tabel validator lagi
                    return  # Kembali ke menu admin setelah menampilkan tabel
                else:
                    print("Invalid choice. Please try again.")
                    continue
        except Exception as e:
            print(f"Error: {e}")
            
    def edit_validator(self, validator_id):
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
            # Validasi email baru
            while True:
                new_email = input(f"Enter new email (current: {validator['email']}): ").strip()
                if not self.auth_controller.is_valid_email(new_email):  # Panggil fungsi validasi email
                    print("Invalid email format. Please enter a valid email address (e.g., example@domain.com).")
                else:
                    break  # Keluar dari loop jika email valid

            # Validasi password baru
            while True:
                new_password = input(f"Enter new password (current: {validator['password']}): ").strip()
                if len(new_password) < 8:
                    print("Password must be at least 8 characters.")
                else:
                    break  # Keluar dari loop jika password valid
            new_instancy = input(f"Enter new instancy (current: {validator['instancy']}): ").strip()

            new_academic_position = input(f"Enter new academic position (current: {validator['academic_position']}): ").strip()
            # Opsi untuk mengedit URL (Scopus, Sinta, Google Scholar)
            while True:
                print("\nDo you want to edit URLs?")
                print("1. Edit Scopus URL")
                print("2. Edit Sinta URL")
                print("3. Edit Google Scholar URL")
                print("4. Skip URL editing")
                url_choice = input("Choose an option: ").strip()
    
                if url_choice == "1":
                    new_scopus_url = self.get_valid_url("Scopus", validator["scopus_url"])
                    validator_data.loc[validator_data["validator_id"] == validator_id, "scopus_url"] = new_scopus_url
                elif url_choice == "2":
                    new_sinta_url = self.get_valid_url("Sinta", validator["sinta_url"])
                    validator_data.loc[validator_data["validator_id"] == validator_id, "sinta_url"] = new_sinta_url
                elif url_choice == "3":
                    new_google_scholar_url = self.get_valid_url("Google Scholar", validator["google_scholar_url"])
                    validator_data.loc[validator_data["validator_id"] == validator_id, "google_scholar_url"] = new_google_scholar_url
                elif url_choice == "4":
                    break  # Keluar dari loop jika tidak ingin mengedit URL
                else:
                    print("Invalid choice. Please try again.")
    
            # Simpan kembali ke file CSV
            self.validator_model.write_data(validator_data)
            print("Validator updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
    
            # Update data validator
            validator_data.loc[validator_data["validator_id"] == validator_id, "username"] = new_username or validator["username"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "full_name"] = new_full_name or validator["full_name"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "email"] = new_email or validator["email"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "password"] = new_password or validator["password"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "instancy"] = new_instancy or validator["instancy"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "academic_position"] = new_academic_position or validator["academic_position"]

            # Simpan kembali ke file CSV
            self.validator_model.write_data(validator_data)
            print("Validator updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
            
    def delete_validator(self, validator_id):
        try:
            # Panggil metode delete_data dari validator_model
            self.validator_model.delete_data("validator_id", validator_id)
            print(f"Validator with ID {validator_id} has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting validator: {e}")

    def delete_user(self, user_id):
        try:
            # Panggil metode delete_data dari user_model
            self.user_model.delete_data("user_id", user_id)
            print(f"User  with ID {user_id} has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting user: {e}")
            
    # Validation Rule
    def get_valid_url(self, url_type, current_url):
        while True:
            print(f"\nCurrent {url_type} URL: {current_url}")
            new_url = input(f"Enter new {url_type} URL (or leave blank to keep current): ").strip()
    
            # Jika pengguna tidak memasukkan URL, kembalikan URL saat ini
            if not new_url:
                return current_url
    
            # Validasi URL
            if not new_url.startswith("http"):
                print(f"Invalid {url_type} URL. It must start with 'http' or 'https'.")
            elif not "." in new_url:  # Minimal harus ada domain (contoh: example.com)
                print(f"Invalid {url_type} URL. It must contain a valid domain.")
            else:
                return new_url  # Kembalikan URL yang valid jika semua validasi terpenuhi