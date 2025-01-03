import pandas as pd
from utils import clear_screen
from tabulate import tabulate

class CheckController:
    def __init__(self, report_file):
        self.report_file = report_file

    def check_journal_url(self, journal_url):
        clear_screen()
        # Validasi URL
        if not journal_url.startswith("http"):
            print("Error: URL harus dimulai dengan 'http'. Silakan coba lagi.")
            return  # Kembali jika URL tidak valid

        try:
            # Membaca data laporan
            report_data = pd.read_csv(self.report_file)

            # Mencari jurnal berdasarkan URL
            journal_info = report_data[report_data["journal_url"] == journal_url]

            if journal_info.empty:
                print("Informasi jurnal tidak ditemukan untuk URL yang diberikan.")
                return

            print("\n=== Laporan dengan URL yang sama ===")
            display_data = journal_info[["report_id", "full_name", "status_laporan", "tanggal_laporan"]]
            print(tabulate(display_data, headers="keys", tablefmt="grid"))

            while True:
                report_id = input("\nMasukkan ID Laporan untuk melihat detail atau 0 untuk kembali: ").strip()
                if report_id == "0":
                    return  # Kembali ke menu utama

                try:
                    report_id = int(report_id)
                    if report_id in journal_info["report_id"].values:
                        selected_report = journal_info[journal_info["report_id"] == report_id].iloc[0]
                        self.display_report_details(selected_report)
                        break 
                    else:
                        print("ID laporan tidak ditemukan. Silakan coba lagi.")
                except ValueError:
                    print("Masukkan ID Laporan untuk melihat detail atau 0 untuk kembali")

        except FileNotFoundError:
            print("File data laporan tidak ditemukan.")
        except Exception as e:
            print(f"Error: {e}")

    def display_report_details(self, report):
        try:
            user_data = pd.read_csv("database/tb_user.csv")
            validator_data = pd.read_csv("database/tb_validator.csv")
    
            user_id = report['user_id']
            validator_id = report['validator_id']
    
            user = user_data[user_data["user_id"] == user_id]
            validator = validator_data[validator_data["validator_id"] == int(validator_id)] if pd.notna(validator_id) else pd.DataFrame()
    
            print("\n=== Detail Laporan ===")
            print(f"ID Laporan: {report['report_id']}")
            print(f"Tanggal Dikirim: {report['tanggal_laporan']}")
            print(f"Nama Jurnal: {report['journal_name']}")
            print(f"URL Jurnal: {report['journal_url']}")
    
            if not user.empty:
                user = user.iloc[0]  # Ambil baris pertama
                print(f"Nama Pelapor: {user['full_name']}")
                print(f"Instansi Pelapor: {user['instancy']}")
            else:
                print("Nama Pelapor: N/A")
                print("Instansi Pelapor: N/A")
    
            print(f"Alasan: {report['reason']}")
    
            print("\n=== Hasil Review ===")
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
    
        except FileNotFoundError:
            print("Error: File database tidak ditemukan.")
        except Exception as e:
            print(f"Error: {e}")