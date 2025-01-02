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
            print("Error: URL must start with 'http'. Please try again.")
            return  # Kembali jika URL tidak valid

        try:
            # Membaca data laporan
            report_data = pd.read_csv(self.report_file)

            # Mencari jurnal berdasarkan URL
            journal_info = report_data[report_data["journal_url"] == journal_url]

            if journal_info.empty:
                print("Journal information not found for the provided URL.")
                return  # Keluar dari fungsi jika jurnal tidak ditemukan

            # Tampilkan tabel semua laporan dengan URL yang sama
            print("\n=== Reports with the Same URL ===")
            display_data = journal_info[["report_id", "full_name", "status_laporan", "tanggal_laporan"]]
            print(tabulate(display_data, headers="keys", tablefmt="grid"))

            # Minta user untuk memilih laporan yang ingin dilihat detailnya
            while True:
                report_id = input("\nEnter Report ID to view details or 0 to return: ").strip()
                if report_id == "0":
                    return  # Kembali ke menu utama

                try:
                    report_id = int(report_id)
                    if report_id in journal_info["report_id"].values:
                        # Ambil detail laporan yang dipilih
                        selected_report = journal_info[journal_info["report_id"] == report_id].iloc[0]
                        self.display_report_details(selected_report)
                        break  # Keluar dari loop setelah menampilkan detail
                    else:
                        print("Invalid Report ID. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid Report ID.")

        except FileNotFoundError:
            print("Report data file not found.")
        except Exception as e:
            print(f"Error: {e}")

    def display_report_details(self, report):
        """Menampilkan detail laporan yang dipilih sesuai format view_report_details."""
        try:
            # Baca semua database sekaligus
            user_data = pd.read_csv("database/tb_user.csv")
            validator_data = pd.read_csv("database/tb_validator.csv")
    
            # Cari data user dan validator berdasarkan ID
            user_id = report['user_id']
            validator_id = report['validator_id']
    
            user = user_data[user_data["user_id"] == user_id]
            validator = validator_data[validator_data["validator_id"] == int(validator_id)] if pd.notna(validator_id) else pd.DataFrame()
    
            # Tampilkan detail laporan
            print("\n=== Report Details ===")
            print(f"Report ID: {report['report_id']}")
            print(f"Date Submitted: {report['tanggal_laporan']}")
            print(f"Journal Name: {report['journal_name']}")
            print(f"Journal URL: {report['journal_url']}")
    
            # Tampilkan nama dan instansi pelapor
            if not user.empty:
                user = user.iloc[0]  # Ambil baris pertama
                print(f"Nama Pelapor: {user['full_name']}")
                print(f"Instansi Pelapor: {user['instancy']}")
            else:
                print("Nama Pelapor: N/A")
                print("Instansi Pelapor: N/A")
    
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
    
        except FileNotFoundError:
            print("Error: Database file not found.")
        except Exception as e:
            print(f"Error: {e}")