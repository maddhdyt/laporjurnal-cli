import pandas as pd
import re
import time
from utils import clear_screen
from datetime import datetime
from tabulate import tabulate

class ReportController:
    def __init__(self, report_file):
        self.report_file = report_file
        self.validator_file = "database/tb_validator.csv"
        
        
    # Validator Function
    def list_pending_reports(self, validator_id):
        print("\n=== Laporan Tersedia ===")
        try:
            report_data = pd.read_csv(self.report_file)

            pending_reports = report_data[report_data["status_laporan"] == "pending"]

            if pending_reports.empty:
                print("Tidak ada laporan yang menunggu untuk diproses.")
                input("\nTekan Enter untuk kembali ke Menu Validator...")
                return

            display_data = pending_reports[["report_id", "tanggal_laporan", "journal_name", "journal_url"]]
            print(tabulate(display_data, headers="keys", tablefmt="grid"))

            report_id = input("\nMasukkan ID Laporan untuk melihat detail, terima, atau 0 untuk kembali: ").strip()
            if report_id == "0":
                return

            try:
                report_id = int(report_id)
            except ValueError:
                print("ID Laporan Tidak Valid. Silakan coba lagi.")
                return

            if report_id in pending_reports["report_id"].values:
                self.view_pending_report_details(report_id, validator_id)
            else:
                print("ID Laporan tidak ditemukan. Silakan coba lagi.")

        except FileNotFoundError:
            print("Tidak ada data laporan yang ditemukan.")
        except Exception as e:
            print(f"Error: {e}")

    def view_pending_report_details(self, report_id, validator_id):
        print("\n=== Detail Laporan Pending ===")

        try:
            report_data = pd.read_csv(self.report_file)

            report = report_data[report_data["report_id"] == report_id]

            if report.empty:
                print("Laporan tidak ditemukan.")
                return

            report = report.iloc[0]

            if report["status_laporan"] != "pending":
                print("Laporan ini tidak dalam status pending dan tidak dapat diterima.")
                return

            reporter_name = "Anonymous" if report["is_anonymous"] else report["full_name"]

            print(f"ID Laporan: {report['report_id']}")
            print(f"Nama Pelapor: {reporter_name}")
            print(f"Nama Jurnal: {report['journal_name']}")
            print(f"URL Jurnal: {report['journal_url']}")
            print(f"Alasan: {report['reason']}")
            print(f"Tanggal Dikirim: {report['tanggal_laporan']}")

            choice = input("\nApakah Anda ingin menerima laporan ini untuk direview? (Y/N): ").strip().lower()
            if choice == "y":
                # memastikan tipe data validator id adalah string
                report_data["validator_id"] = report_data["validator_id"].fillna("").astype(str)

                report_data.loc[report_data["report_id"] == report_id, "status_laporan"] = "review"
                report_data.loc[report_data["report_id"] == report_id, "validator_id"] = str(validator_id)
                report_data.to_csv(self.report_file, index=False)
                print(f"ID Laporan {report_id} telah diterima untuk direview.")
            else:
                print("Laporan tidak diterima.")

            input("\nTekan Enter untuk kembali ke Menu Validator...")

        except FileNotFoundError:
            print("Tidak ada data laporan yang ditemukan.")
        except Exception as e:
            print(f"Error: {e}")
    
    def list_accepted_reports(self, validator_id):
        print("\n=== Laporan Diterima ===")
        try:
            report_data = pd.read_csv(self.report_file)

            report_data["validator_id"] = report_data["validator_id"].fillna("").apply(
                lambda x: str(int(x)) if x != "" else ""
            )
            report_data["status_laporan"] = report_data["status_laporan"].fillna("")

            accepted_reports = report_data[
                (report_data["validator_id"] == str(validator_id)) &
                (report_data["status_laporan"].isin(["review", "done"]))
            ]

            if accepted_reports.empty:
                print("Anda tidak memiliki laporan yang diterima.")
                print("Halaman ini akan tetap tersedia untuk laporan di masa depan.")
                input("\nTekan Enter untuk kembali ke Menu Validator...")
                return

            from tabulate import tabulate
            display_data = accepted_reports[[
                "report_id", "journal_name", "status_laporan", "tanggal_laporan"
            ]]
            print(tabulate(display_data, headers="keys", tablefmt="grid"))

            report_id = input("\nMasukkan ID Laporan untuk mengelola atau 0 untuk kembali: ").strip()
            if report_id == "0":
                return

            try:
                report_id = int(report_id)
            except ValueError:
                print("ID Laporan Tidak Valid. Silakan coba lagi.")
                return

            if report_id in accepted_reports["report_id"].values:
                selected_report = accepted_reports[accepted_reports["report_id"] == report_id].iloc[0].to_dict()
                self.manage_report(selected_report, validator_id)  # Pastikan validator_id dikirim
            else:
                print("ID Laporan Tidak Valid. Silakan coba lagi.")

        except FileNotFoundError:
            print("Tidak ada file data laporan yang ditemukan.")
            input("\nTekan Enter untuk kembali ke Menu Validator...")
        except Exception as e:
            print(f"Error: {e}")
            input("\nTekan Enter untuk kembali ke Menu Validator...")

    def update_report(self, report):
        print("\n=== Perbarui Laporan ===")
        
        print(f"ID Laporan: {report['report_id']}")
        print(f"Status Jurnal Saat Ini: {report['status_jurnal'] if not pd.isna(report['status_jurnal']) else 'N/A'}")
        
        new_status = input("Masukkan status jurnal baru (aman, predator, clone): ").strip().lower()
        if new_status not in ["aman", "predator", "clone"]:
            print("Status tidak valid. Silakan pilih dari aman, predator, atau clone.")
            return

        # Meminta input untuk feedback baru
        new_feedback = input("Masukkan umpan balik baru: ").strip()

        try:
            # Baca data laporan
            report_data = pd.read_csv(self.report_file)

            # Update status_jurnal dan feedback
            report_data.loc[report_data["report_id"] == report["report_id"], "status_jurnal"] = new_status
            report_data.loc[report_data["report_id"] == report["report_id"], "feedback"] = new_feedback

            # Simpan kembali ke file CSV
            report_data.to_csv(self.report_file, index=False)
            print("Laporan berhasil diperbarui.")

        except Exception as e:
            print(f"Error: {e}")

    def manage_report(self, report, validator_id):
        while True:
            report_data = pd.read_csv(self.report_file)
            updated_report = report_data[report_data["report_id"] == report["report_id"]].iloc[0].to_dict()

            print("\n=== Kelola Laporan ===")
            print(f"ID Laporan: {updated_report['report_id']}")
            print(f"Nama Pelapor: {updated_report['full_name'] if not updated_report['is_anonymous'] else 'Anonymous'}")
            print(f"Nama Jurnal: {updated_report['journal_name']}")
            print(f"URL Jurnal: {updated_report['journal_url']}")
            print(f"Alasan: {updated_report['reason']}")
            print(f"Status Laporan: {updated_report['status_laporan']}")
            print(f"Status Jurnal: {updated_report['status_jurnal'] if not pd.isna(updated_report['status_jurnal']) else 'N/A'}")
            print(f"Umpan Balik: {updated_report['feedback'] if not pd.isna(updated_report['feedback']) else 'N/A'}")
            print(f"Tanggal Dikirim: {updated_report['tanggal_laporan']}")

            print("\nOpsi:")
            
            if updated_report['status_laporan'] == 'review':
                print("1. Validasi Laporan")
                print("2. Tandai Sebagai Pending")
                print("3. Kembali ke Laporan yang Diterima")
            elif updated_report['status_laporan'] == 'done':
                print("1. Perbarui Laporan")
                print("2. Kembali ke Laporan yang Diterima")

            choice = input("Pilih Opsi: ").strip()

            if choice == "1":
                if updated_report['status_laporan'] == 'review':
                    self.validate_report(updated_report)
                    self.list_accepted_reports(validator_id)
                    return
                elif updated_report['status_laporan'] == 'done':
                    self.update_report(updated_report)
                    self.list_accepted_reports(validator_id)
                    return
            elif choice == "2":
                if updated_report['status_laporan'] == 'review':
                    self.mark_as_pending(updated_report)
                    self.list_accepted_reports(validator_id)
                    return
                elif updated_report['status_laporan'] == 'done':
                    self.list_accepted_reports(validator_id)
                    return
            elif choice == "3":
                self.list_accepted_reports(validator_id)
                return
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

    def validate_report(self, report):
        print("\n=== Validasi Laporan ===")

        print("Opsi: aman, predator, clone")
        new_status = input("Masukkan status jurnal baru: ").strip().lower()
        if new_status not in ["aman", "predator", "clone"]:
            print("Status tidak valid. Silakan pilih dari aman, predator, atau clone.")
            return

        new_feedback = input("Masukkan umpan balik Anda: ").strip()

        try:
            report_data = pd.read_csv(self.report_file)

            # Pastikan tipe data kolom status_jurnal dan feedback adalah string
            report_data['status_jurnal'] = report_data['status_jurnal'].astype(str)
            report_data['feedback'] = report_data['feedback'].astype(str)

            report_data.loc[report_data["report_id"] == report["report_id"], "status_jurnal"] = new_status
            report_data.loc[report_data["report_id"] == report["report_id"], "feedback"] = new_feedback
            report_data.loc[report_data["report_id"] == report["report_id"], "status_laporan"] = "done"

            report_data.to_csv(self.report_file, index=False)
            print("Laporan berhasil divalidasi. Status telah diperbarui menjadi 'done'.")
            input("\nTekan Enter untuk kembali ke Laporan yang Diterima...")

        except Exception as e:
            print(f"Error: {e}")

    def mark_as_pending(self, report):
        print("\n=== Tandai Sebagai Pending ===")
        confirm = input("Apakah Anda yakin ingin menandai laporan ini sebagai pending? (Y/N): ").strip().lower()

        if confirm != "y":
            print("Operasi dibatalkan.")
            return

        try:
            # Baca data laporan
            report_data = pd.read_csv(self.report_file)

            # Update status_laporan dan hapus validator_id
            report_data.loc[report_data["report_id"] == report["report_id"], "status_laporan"] = "pending"
            report_data.loc[report_data["report_id"] == report["report_id"], "validator_id"] = None
            report_data.to_csv(self.report_file, index=False)

            print("Laporan berhasil ditandai sebagai pending.")
            input("\nTekan Enter untuk kembali ke Menu Validator...")
            raise StopIteration  # Digunakan untuk keluar dari loop manage_report

        except StopIteration:
            return  # Kembali langsung ke Validator Menu
        except Exception as e:
            print(f"Error: {e}")

    def accept_report(self, report, validator_id):
        print("\n=== Terima Laporan ===")
        try:
            report_data = pd.read_csv(self.report_file)

            report_data.loc[report_data["report_id"] == report["report_id"], "validator_id"] = validator_id
            report_data.loc[report_data["report_id"] == report["report_id"], "status_laporan"] = "review"

            report_data.to_csv(self.report_file, index=False)
            print(f"ID Laporan {report['report_id']} telah diterima untuk direview.")
        except Exception as e:
            print(f"Error: {e}")
            
    def show_validator_statistics(self, validator_id):
        try:
            report_data = pd.read_csv(self.report_file)

            total_pending = len(report_data[report_data["status_laporan"] == "pending"])
            total_review = len(report_data[(report_data["status_laporan"] == "review") & (report_data["validator_id"] == validator_id)])
            total_done = len(report_data[(report_data["status_laporan"] == "done") & (report_data["validator_id"] == validator_id)])
            total_handled = total_review + total_done

            print("\n=== Statistik Validator ===")
            print(f"Total Laporan Tersedia: {total_pending}")
            print(f"Laporan yang Sedang Direview: {total_review}")
            print(f"Laporan yang Sudah Selesai: {total_done}")
            print(f"Total Laporan Ditangani: {total_handled}")

        except FileNotFoundError:
            print("Tidak ada data laporan yang ditemukan..")
        except Exception as e:
            print(f"Error: {e}")

    #User Function
    def report_journal(self, user_id, full_name):
        clear_screen()
        print("\n=== Laporan Jurnal ===")

        while True:
            is_anonymous_input = input("Apakah anda ingin melaporkan secara anonim? (Y/N): ").strip().lower()
            if is_anonymous_input == "y":
                is_anonymous = True
                reporter_name = "Anonymous"
                break
            elif is_anonymous_input == "n":
                is_anonymous = False
                reporter_name = full_name
                break
            else:
                print("Pilihan tidak valid. Silakan masukkan Y atau N.")

        while True:
            journal_name = input("Masukkan nama jurnal: ").strip()
            if journal_name: 
                break
            else:
                print("Nama jurnal tidak boleh kosong. Silakan coba lagi.")

        while True:
            journal_url = input("Masukkan URL jurnal: ").strip()
            if self.is_valid_url(journal_url):
                break
            else:
                print("URL tidak valid. Silakan masukkan URL yang valid dimulai dengan 'http://' atau 'https://', mengandung domain, dan tanpa spasi.")

        while True:
            reason = input("Masukkan alasan pelaporan Anda: ").strip()
            if reason:  
                break
            else:
                print("Alasan tidak boleh kosong. Silakan coba lagi.")

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

        report_data.to_csv(self.report_file, index=False)

        print("\nLaporan berhasil dikirim!")
        print("\n=== Laporan Yang Telah Dikirim ===")
        display_report = {key: value for key, value in new_report.items() if key != "is_anonymous"}  # Exclude is_anonymous
        print(tabulate([display_report.values()], headers=display_report.keys(), tablefmt="grid"))
        
    def track_reports(self, user_id):
        clear_screen()
        while True:
            print("\n=== Pelacakan Laporan ===")
            try:
                report_data = pd.read_csv(self.report_file)

                user_reports = report_data[report_data["user_id"] == user_id]

                if user_reports.empty:
                    print("Anda tidak memiliki laporan untuk dilacak.")
                    return 
                
                display_data = user_reports[[
                    "report_id", "journal_name", "status_laporan", "tanggal_laporan"
                ]]
                print(tabulate(display_data, headers="keys", tablefmt="grid"))

                report_id = input("\nMasukkan ID Laporan untuk melihat detail atau 0 untuk kembali: ").strip()
                if report_id == "0":
                    return  

                try:
                    report_id = int(report_id)
                except ValueError:
                    print("ID Laporan Tidak Valid. Silakan coba lagi.")
                    continue 

                if report_id in user_reports["report_id"].values:
                    selected_report = user_reports[user_reports["report_id"] == report_id].iloc[0].to_dict()
                    
                    self.view_report_details(selected_report)
                    
                    if selected_report["status_laporan"] == "pending":
                        edit_choice = input("\nTekan 1 untuk mengedit laporan ini atau 0 untuk kembali ke Pelacakan Laporan: ").strip()
                        if edit_choice == '1':
                            self.edit_report(selected_report)
                        elif edit_choice == '0':
                            continue  # melanjut loop
                        else:
                            print("Pilihan tidak valid. Kembali ke Pelacakan Laporan...")
                    else:
                        print("\nLaporan ini tidak dapat diedit karena statusnya bukan pending")
                        input("\nTekan Enter untuk kembali ke Pelacakan Laporan...")
                        clear_screen()

                else:
                    print("ID Laporan Tidak Valid. Silakan coba lagi.")

            except FileNotFoundError:
                print("Tidak ada file yang ditemukan.")
                return
            except Exception as e:
                print(f"Error: {e}")        

    def view_report_details(self, report):
        clear_screen()
        print("\n=== Detail Laporan ===")
        try:
            print(f"ID Laporan: {report['report_id']}")
            print(f"Nama Jurnal: {report['journal_name']}")
            print(f"URL Jurnal: {report['journal_url']}")
            print(f"Alasan: {report['reason']}")
            print(f"Status Laporan: {report['status_laporan']}")
            print(f"Status Jurnal: {report['status_jurnal'] if not pd.isna(report['status_jurnal']) else 'N/A'}")
            print(f"Umpan Balik: {report['feedback'] if not pd.isna(report['feedback']) else 'N/A'}")
            print(f"Tanggal Dikirim: {report['tanggal_laporan']}")

            # Check if the report has been assigned to a validator
            if not pd.isna(report["validator_id"]):
                validator_data = pd.read_csv("database/tb_validator.csv")

                validator = validator_data[validator_data["validator_id"] == int(report["validator_id"])]
                if not validator.empty:
                    validator = validator.iloc[0]  # Get the first match
                    print("\n=== Informasi Validator ===")
                    print(f"Nama Validator: {validator['full_name']}")
                    print(f"Validator Email: {validator['email']}")
                    print(f"Validator Instansi: {validator['instancy']}")
                    print(f"Validator Posisi Akademik: {validator['academic_position']}")
                    print(f"Scopus Profil: {validator['sinta_url']}")
                    print(f"Sinta Profil: {validator['scopus_url']}")
                    print(f"Google Scholar Profil: {validator['google_scholar_url']}")
                else:
                    print("\nTidak ada informasi validator.")
            else:
                print("\nLaporan ini belum ditugaskan kepada validator.")

        except Exception as e:
            print(f"Error: {e}")
            
    def edit_report(self, report):
        clear_screen()
        print("\n=== Edit Laporan ===")
        print(f"Nama Jurnal Saat Ini: {report['journal_name']}")
        print(f"URL Jurnal Saat Ini: {report['journal_url']}")
        print(f"Alasan Saat Ini: {report['reason']}")
        print("\nOpsi:")
        print("1. Edit Laporan")
        print("2. Hapus Laporan")
        print("0. Kembali ke Pelacakan Laporan")

        choice = input("Pilih opsi: ").strip()

        if choice == "1":
            new_journal_name = input("Masukkan nama jurnal baru (kosongkan untuk mempertahankan yang saat ini): ").strip()
            
            while True:
                new_journal_url = input("Masukkan URL jurnal baru (kosongkan untuk mempertahankan yang saat ini): ").strip()
                if not new_journal_url:
                    break
                elif not self.is_valid_url(new_journal_url):
                    print("URL tidak valid. Silakan masukkan URL yang valid dimulai dengan 'http://' atau 'https://', mengandung domain, dan tanpa spasi.")
                else:
                    break
            
            new_reason = input("Masukkan alasan baru (kosongkan untuk mempertahankan yang saat ini): ").strip()

            if new_journal_name:
                report['journal_name'] = new_journal_name
            if new_journal_url:
                report['journal_url'] = new_journal_url
            if new_reason:
                report['reason'] = new_reason

            try:
                report_data = pd.read_csv(self.report_file)

                report_data.loc[report_data["report_id"] == report["report_id"], "journal_name"] = report['journal_name']
                report_data.loc[report_data["report_id"] == report["report_id"], "journal_url"] = report['journal_url']
                report_data.loc[report_data["report_id"] == report["report_id"], "reason"] = report['reason']

                # Simpan kembali ke file CSV
                report_data.to_csv(self.report_file, index=False)
                print("Laporan berhasil diperbarui. Redirecting...")
                time.sleep(2)

                self.view_report_details(report)  # Tampilkan detail setelah edit

            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            if report["status_laporan"] == "pending":
                confirm = input("Apakah Anda yakin ingin menghapus laporan ini? (Y/N): ").strip().lower()
                if confirm == "y":
                    try:
                        report_data = pd.read_csv(self.report_file)
                        report_data = report_data[report_data["report_id"] != report["report_id"]]
                        
                        report_data.to_csv(self.report_file, index=False)
                        print("Laporan berhasil dihapus, Redirecting...")
                        time.sleep(2)
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Penghapusan dibatalkan.")
            else:
                print("Anda hanya dapat menghapus laporan dengan status 'pending'.")

        elif choice == "0":
            return  # Kembali ke menu Tracking Reports
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            
    def view_user_statistics(self, user_id):
        try:
            report_data = pd.read_csv(self.report_file)

            user_reports = report_data[report_data["user_id"] == user_id]

            total_reports = len(user_reports)  # Total Laporan
            pending_reports = len(user_reports[user_reports["status_laporan"] == "pending"])  # Laporan Pending
            review_reports = len(user_reports[user_reports["status_laporan"] == "review"])  # Laporan Review
            done_reports = len(user_reports[user_reports["status_laporan"] == "done"])  # Laporan Sukses

            print("=== Statistik Laporan Anda ===")
            print(f"Total Laporan: {total_reports}")
            print(f"Laporan Pending: {pending_reports}")
            print(f"Laporan Review: {review_reports}")
            print(f"Laporan Sukses: {done_reports}")

        except FileNotFoundError:
            print("Tidak ada file data laporan yang ditemukan..")
        except Exception as e:
            print(f"Error: {e}")
            
    # Validation Rule
    def is_valid_url(self, url):
        """Validasi URL menggunakan regex."""
        return re.match(r"^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/[^ ]*)?$", url) is not None and ' ' not in url