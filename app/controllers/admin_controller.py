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
            done_reports = len(report_data[report_data["status_laporan"] == "sukses"])  # Laporan Sukses

            # Tampilkan statistik dalam format yang rapi
            print("=== Statistik ===")
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
            print("\n=== Semua Laporan ===")
            try:
                report_data = self.report_model.read_data()
                if report_data.empty:
                    print("Tidak ada laporan yang ditemukan.")
                    return  
                else:
                    display_data = report_data[["report_id", "journal_name", "journal_url", "status_laporan"]]
                    print(tabulate(display_data, headers="keys", tablefmt="fancy_grid"))

                    while True:
                        report_id = input("\nMasukkan ID Laporan untuk melihat detail atau 0 untuk kembali: ").strip()
                        if report_id == "0":
                            return
                        elif report_id.isdigit():
                            report_id = int(report_id)
                            if report_id in report_data["report_id"].values:
                                self.view_report_details(report_id)
                                break 
                            else:
                                print("ID laporan tidak ditemukan. Silakan coba lagi.")
                        else:
                            print("Masukan tidak valid. Masukkan ID Laporan yang valid atau 0 untuk kembali.")
            except Exception as e:
                print(f"Error: {e}")

    def view_report_details(self, report_id):
        try:
            # Baca data laporan
            report_data = self.report_model.read_data()
            report = report_data[report_data["report_id"] == report_id]
    
            if report.empty:
                print("Laporan tidak ditemukan.")
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
            print("\n=== Rincian Laporan ===")
            print(f"ID Laporan: {report['report_id']}")
            print(f"Tanggal Dikirim: {report['tanggal_laporan']}")
            print(f"Nama Jurnal: {report['journal_name']}")
            print(f"URL Jurnal: {report['journal_url']}")
            print(f"Nama Pelapor: {user.iloc[0]['full_name'] if not user.empty else 'N/A'}")
            print(f"Instansi Pelapor: {user.iloc[0]['instancy'] if not user.empty else 'N/A'}")
            print(f"Alasan: {report['reason']}")
    
            # Tampilkan hasil review (jika ada)
            print("\n=== Review Result ===")
            if not validator.empty:
                validator = validator.iloc[0]  # Ambil baris pertama
                print(f"Nama Validator: {validator['full_name']}")
                print(f"Instansi Validator: {validator['instancy']}")
                print("Profil Validator:")
                if pd.notna(validator['scopus_url']):
                    print(f"- {validator['scopus_url']}")
                if pd.notna(validator['sinta_url']):
                    print(f"- {validator['sinta_url']}")
                if pd.notna(validator['google_scholar_url']):
                    print(f"- {validator['google_scholar_url']}")
            else:
                print("Nama Validator: N/A")
                print("Instansi Validator: N/A")
                print("Profil Validator: N/A")
    
            print(f"Status Laporan: {report['status_laporan']}")
            print(f"Status Jurnal: {report['status_jurnal'] if not pd.isna(report['status_jurnal']) else 'N/A'}")
            print(f"Umpan Balik: {report['feedback'] if not pd.isna(report['feedback']) else 'N/A'}")
            
            # Opsi untuk kembali ke daftar laporan
            while True:
                choice = input("\nTekan 0 untuk kembali ke daftar laporan: ").strip()
                if choice == "0":
                    return  # Kembali ke daftar laporan
                else:
                    print("Input tidak valid. Silakan tekan 0 untuk kembali.")
        except Exception as e:
            print(f"Error: {e}")

    def view_all_users(self):
        clear_screen()
        print("\n=== Semua Pengguna ===")
        try:
            user_data = self.user_model.read_data()
            if user_data.empty:
                print("Tidak ada pengguna yang ditemukan.")
                return  # Kembali ke menu sebelumnya jika tidak ada data user
            else:
                # Tampilkan hanya kolom user_id, full_name, dan instancy
                display_data = user_data[["user_id", "full_name", "instancy"]]
                print(tabulate(display_data, headers="keys", tablefmt="fancy_grid"))

                while True:
                    # Meminta admin untuk memasukkan user_id untuk melihat detail atau menghapus
                    user_id = input("\nMasukkan ID Pengguna untuk melihat detail, hapus, atau 0 untuk kembali: ").strip()

                    # Validasi input: harus berupa angka
                    if not user_id.isdigit():
                        print("Masukan tidak valid. Masukkan ID Pengguna (angka) yang valid atau 0 untuk kembali.")
                        continue  # Lanjutkan loop untuk meminta input lagi

                    user_id = int(user_id)  # Konversi input ke integer

                    if user_id == 0:
                        return  # Kembali ke menu admin langsung
                    elif user_id in user_data["user_id"].values:
                        # Tampilkan detail pengguna
                        self.view_user_details(user_id)
                        break  # Keluar dari loop setelah kembali dari view_user_details
                    else:
                        print("ID pengguna tidak ditemukan. Silakan coba lagi.")
        except Exception as e:
            print(f"Error: {e}")

    def view_user_details(self, user_id):
        clear_screen()
        try:
            user_data = self.user_model.read_data()
            user = user_data[user_data["user_id"] == user_id]

            if user.empty:
                print("Pengguna tidak ditemukan.")
                return

            # Ambil informasi pengguna
            user = user.iloc[0]  # Ambil baris pertama
            print("\n=== Detail Pengguna ===")
            print(f"ID Pengguna: {user['user_id']}")
            print(f"Username: {user['username']}")
            print(f"Nama Lengkap: {user['full_name']}")
            print(f"Email: {user['email']}")
            print(f"Password: {user['password']}")
            print(f"Instansi: {user['instancy']}")
            print(f"Peran: {user['role']}")

            # Loop untuk memastikan input yang valid
            while True:
                print("\nOpsi:")
                print("1. Hapus Pengguna")
                print("2. Kembali ke Daftar Pengguna")
                choice = input("Pilih opsi: ").strip()

                if choice == "1":
                    self.delete_user(user_id)
                    break  # Keluar dari loop setelah menghapus pengguna
                elif choice == "2":
                    # Tampilkan tabel pengguna lagi
                    self.view_all_users()
                    return  # Kembali ke menu admin setelah menampilkan tabel
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")
                    # Loop akan berlanjut hingga input yang valid diberikan

        except Exception as e:
            print(f"Error: {e}")

    def view_all_validators(self):
        clear_screen()
        print("\n=== Semua Validator ===")
        try:
            validator_data = self.validator_model.read_data()
            if validator_data.empty:
                print("Tidak ada validator yang ditemukan.")
                return  # Kembali ke menu sebelumnya jika tidak ada data validator
            else:
                # Tampilkan hanya kolom validator_id, full_name, dan instancy
                display_data = validator_data[["validator_id", "full_name", "instancy"]]
                print(tabulate(display_data, headers="keys", tablefmt="fancy_grid"))

                while True:
                    # Meminta admin untuk memasukkan validator_id untuk melihat detail atau menghapus
                    validator_id = input("\nMasukkan ID Validator untuk melihat detail, hapus, atau 0 untuk kembali: ").strip()

                    # Validasi input: harus berupa angka
                    if not validator_id.isdigit():
                        print("Masukan tidak valid. Masukkan ID Validator (angka) yang valid atau 0 untuk kembali.")
                        continue  # Lanjutkan loop untuk meminta input lagi

                    validator_id = int(validator_id)  # Konversi input ke integer

                    if validator_id == 0:
                        return  # Kembali ke menu admin langsung
                    elif validator_id in validator_data["validator_id"].values:
                        # Tampilkan detail validator
                        self.view_validator_details(validator_id)
                        break  # Keluar dari loop setelah kembali dari view_validator_details
                    else:
                        print("ID validator tidak ditemukan. Silakan coba lagi.")
        except Exception as e:
            print(f"Error: {e}")

    def view_validator_details(self, validator_id):
        try:
            validator_data = self.validator_model.read_data()
            validator = validator_data[validator_data["validator_id"] == validator_id]

            if validator.empty:
                print("Pilihan tidak valid. Silakan coba lagi.")
                return

            # Ambil informasi validator
            validator = validator.iloc[0]  # Ambil baris pertama
            print("\n=== Detail Validator ===")
            print(f"ID Validator: {validator['validator_id']}")
            print(f"Username: {validator['username']}")
            print(f"Nama Lengkap: {validator['full_name']}")
            print(f"Email: {validator['email']}")
            print(f"Password: {validator['password']}")
            print(f"Instansi: {validator['instancy']}")
            print(f"Posisi Akademik: {validator['academic_position']}")
            print(f"Scopus URL: {validator['scopus_url']}")
            print(f"Sinta URL: {validator['sinta_url']}")
            print(f"Google Scholar URL: {validator['google_scholar_url']}")

            # Opsi untuk mengedit atau menghapus validator
            while True:
                print("\nOpsi:")
                print("1. Edit Informasi Validator")
                print("2. Edit Password Validator")
                print("3. Hapus Validator")
                print("4. Kembali ke Daftar Validator")
                choice = input("Pilih opsi: ").strip()

                if choice == "1":
                    self.edit_validator_information(validator_id)  # Panggil metode edit_validator_information
                    return
                    
                elif choice == "2":
                    self.edit_validator_password(validator_id)  # Panggil metode edit_validator_password
                    return
                
                elif choice == "3":
                    self.delete_validator(validator_id)  # Panggil metode delete_validator
                    return
                
                elif choice == "4":
                    self.view_all_validators()  # Tampilkan tabel validator lagi
                    return  # Kembali ke menu admin setelah menampilkan tabel
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")
                    continue
        except Exception as e:
            print(f"Error: {e}")
            
    def edit_validator_information(self, validator_id):
        try:
            # Baca data validator dari file CSV
            validator_data = self.validator_model.read_data()
            validator = validator_data[validator_data["validator_id"] == validator_id]

            if validator.empty:
                print("Pilihan tidak valid. Silakan coba lagi.")
                return

            # Ambil informasi validator
            validator = validator.iloc[0]  # Ambil baris pertama
            print("\n=== Edit Validator ===")
            print(f"ID Validator: {validator['validator_id']} (Tidak dapat diubah)")

            # Input untuk mengedit data
            while True:
                new_username = input(f"Masukkan username baru (Saat ini: {validator['username']}): ").strip()
                if new_username:
                    if not self.auth_controller.is_valid_username(new_username):
                        print("Username tidak valid. Username harus terdiri dari minimal 8 karakter dan hanya boleh terdiri dari huruf, angka, '_', dan '.'")
                        continue
                    if new_username != validator["username"] and new_username in validator_data["username"].values:
                        print("Username sudah digunakan. Silakan coba lagi.")
                        continue
                break

            new_full_name = input(f"Masukkan nama lengkap baru (Saat ini: {validator['full_name']}): ").strip()
            
            # Validasi email baru
            # Validasi email baru
            while True:
                new_email = input(f"Masukkan email baru (Saat ini: {validator['email']}): ").strip()
                if new_email:
                    if not self.auth_controller.is_valid_email(new_email):  # Panggil fungsi validasi email
                        print("Format email tidak valid. Masukkan alamat email yang valid (misalnya, example@domain.com).")
                    elif new_email != validator["email"] and new_email in validator_data["email"].values:
                        print("Email sudah digunakan. Silakan pilih email lain.")
                    else:
                        break  # Keluar dari loop jika email valid
                else:
                    break  # Keluar dari loop jika pengguna tidak memasukkan email baru
                
            new_instancy = input(f"Masukkan instansi baru (Saat ini: {validator['instancy']}): ").strip()
            new_academic_position = input(f"Masukkan posisi akademik baru (Saat ini: {validator['academic_position']}): ").strip()
            
            # Opsi untuk mengedit URL (Scopus, Sinta, Google Scholar)
            while True:
                print("\nOpsi untuk mengedit URL:")
                print("1. Edit Scopus URL")
                print("2. Edit Sinta URL")
                print("3. Edit Google Scholar URL")
                print("4. Lewati pengeditan URL")
                url_choice = input("Pilih opsi: ").strip()
    
                if url_choice == "1":
                    new_scopus_url = self.auth_controller.get_valid_url("Scopus", validator["scopus_url"])
                    validator_data.loc[validator_data["validator_id"] == validator_id, "scopus_url"] = new_scopus_url
                elif url_choice == "2":
                    new_sinta_url = self.auth_controller.get_valid_url("Sinta", validator["sinta_url"])
                    validator_data.loc[validator_data["validator_id"] == validator_id, "sinta_url"] = new_sinta_url
                elif url_choice == "3":
                    new_google_scholar_url = self.auth_controller.get_valid_url("Google Scholar", validator["google_scholar_url"])
                    validator_data.loc[validator_data["validator_id"] == validator_id, "google_scholar_url"] = new_google_scholar_url
                elif url_choice == "4":
                    break  # Keluar dari loop jika tidak ingin mengedit URL
                else:
                    print("Pilihan tidak valid, silakan coba lagi.")
    
            # Update data validator
            validator_data.loc[validator_data["validator_id"] == validator_id, "username"] = new_username or validator["username"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "full_name"] = new_full_name or validator["full_name"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "email"] = new_email or validator["email"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "instancy"] = new_instancy or validator["instancy"]
            validator_data.loc[validator_data["validator_id"] == validator_id, "academic_position"] = new_academic_position or validator["academic_position"]
            
            self.validator_model.write_data(validator_data)
            
            # Tampilkan validator details yang terbaru
            validator_data = self.validator_model.read_data()
            validator = validator_data[validator_data["validator_id"] == validator_id].iloc[0]

            print("\n=== Detail Validator ===")
            print(f"ID Validator: {validator['validator_id']}")
            print(f"Username: {validator['username']}")
            print(f"Nama Lengkap: {validator['full_name']}")
            print(f"Email: {validator['email']}")
            print(f"Password: {validator['password']}")
            print(f"Instansi: {validator['instancy']}")
            print(f"Posisi Akademik: {validator['academic_position']}")
            print(f"Scopus URL: {validator['scopus_url']}")
            print(f"Sinta URL: {validator['sinta_url']}")
            print(f"Google Scholar URL: {validator['google_scholar_url']}")

            # Opsi untuk mengedit atau menghapus validator
            print(f"===" + "Informasi Validator Berhasil Diubah" + "===")
            while True:
                print("\nOpsi:")
                print("1. Edit Informasi Validator")
                print("2. Edit Password Validator")
                print("3. Hapus Validator")
                print("4. Kembali ke Daftar Validator")
                choice = input("Pilih opsi: ").strip()

                if choice == "1":
                    self.edit_validator_information(validator_id)  # Panggil metode edit_validator_information
                    return
                    
                elif choice == "2":
                    self.edit_validator_password(validator_id)  # Panggil metode edit_validator_password
                    return
                
                elif choice == "3":
                    self.delete_validator(validator_id) # Panggil metode delete_validator
                    return

                elif choice == "4":
                    self.view_all_validators()  # Tampilkan tabel validator lagi
                    return  # Kembali ke menu admin setelah menampilkan tabel
                else:
                    print("Pilihan tidak valid, silakan coba lagi.")
                    continue
        except Exception as e:
            print(f"Error: {e}")
            
    def edit_validator_password(self, validator_id):
        try:
            # Baca data validator dari file CSV
            validator_data = self.validator_model.read_data()
            validator = validator_data[validator_data["validator_id"] == validator_id]

            if validator.empty:
                print("Validator tidak ditemukan.")
                return

            # Ambil informasi validator
            validator = validator.iloc[0]  # Ambil baris pertama
            print("\n=== Edit Validator Password ===")

            # Minta password yang sekarang
            while True:
                current_password = input("Masukkan password yang sekarang: ").strip()
                if current_password == validator["password"]:
                    break
                else:
                    print("Password yang sekarang tidak benar. Silakan coba lagi.")
            
            while True:
                new_password = input("Masukkan password baru: ").strip()
                if self.auth_controller.is_valid_password(new_password):
                    break
                else:
                    print("Password tidak valid. Password harus terdiri dari minimal 8 karakter dan berisi campuran huruf, angka, dan karakter khusus.")

            # Update password
            validator_data.loc[validator_data["validator_id"] == validator_id, "password"] = new_password

            # Simpan perubahan ke file CSV
            self.validator_model.write_data(validator_data)
            
            # Tampilkan validator details yang terbaru
            validator_data = self.validator_model.read_data()
            validator = validator_data[validator_data["validator_id"] == validator_id].iloc[0]

            print("\n=== Detail Validator ===")
            print(f"ID Validator: {validator['validator_id']}")
            print(f"Username: {validator['username']}")
            print(f"Nama Lengkap: {validator['full_name']}")
            print(f"Email: {validator['email']}")
            print(f"Password: {validator['password']}")
            print(f"Instansi: {validator['instancy']}")
            print(f"Posisi Akademik: {validator['academic_position']}")
            print(f"Scopus URL: {validator['scopus_url']}")
            print(f"Sinta URL: {validator['sinta_url']}")
            print(f"Google Scholar URL: {validator['google_scholar_url']}")

            # Opsi untuk mengedit atau menghapus validator
            print("===" + "Password Validator Berhasil Diubah" + "===")
            while True:
                print("\nOpsi:")
                print("1. Edit Informasi Validator")
                print("2. Edit Password Validator")
                print("3. Hapus Validator")
                print("4. Kembali ke Daftar Validator")
                choice = input("Pilih opsi: ").strip()

                if choice == "1":
                    self.edit_validator_information(validator_id)  # Panggil metode edit_validator_information
                    return
                    
                elif choice == "2":
                    self.edit_validator_password(validator_id)  # Panggil metode edit_validator_password
                    return
                
                elif choice == "3":
                    self.delete_validator(validator_id)  # Panggil metode delete_validator
                    return

                elif choice == "4":
                    self.view_all_validators()  # Tampilkan tabel validator lagi
                    return  # Kembali ke menu admin setelah menampilkan tabel
                else:
                    print("Pilihan tidak valid, silakan coba lagi.")
                    continue
        except Exception as e:
            print(f"Error: {e}")            

            
    def delete_validator(self, validator_id):
        try:
            # Panggil metode delete_data dari validator_model
            self.validator_model.delete_data("validator_id", validator_id)
            print(f"Validator dengan ID {validator_id} berhasil dihapus.")
        except Exception as e:
            print(f"Error: {e}")

    def delete_user(self, user_id):
        try:
            # Panggil metode delete_data dari user_model
            self.user_model.delete_data("user_id", user_id)
            print(f"Pengguna dengan ID {user_id} berhasil dihapus.")
        except Exception as e:
            print(f"Error: {e}")
