import pandas as pd

class CheckController:
    def __init__(self, report_file):
        self.report_file = report_file

    def check_journal_url(self, journal_url):
        """Memeriksa apakah URL jurnal tersedia dalam tb_report.csv."""
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
            else:
                # Ambil informasi jurnal
                journal_info = journal_info.iloc[0]  # Ambil baris pertama
                print("\n=== Journal Information ===")
                print(f"Report ID: {journal_info['report_id']}")
                print(f"Full Name: {journal_info['full_name']}")
                print(f"Journal Name: {journal_info['journal_name']}")
                print(f"Journal URL: {journal_info['journal_url']}")
                print(f"Reason: {journal_info['reason']}")
                print(f"Status: {journal_info['status_laporan']}")
                print(f"Date Submitted: {journal_info['tanggal_laporan']}")
                print(f"Feedback: {journal_info['feedback'] if not pd.isna(journal_info['feedback']) else 'N/A'}")
            
            # Baca data validator
            validator_data = pd.read_csv("database/tb_validator.csv")
            validator_id = journal_info['validator_id']

            # Temukan validator berdasarkan validator_id
            if pd.notna(validator_id):
                validator_info = validator_data[validator_data["validator_id"] == int(validator_id)]
                if not validator_info.empty:
                    validator_info = validator_info.iloc[0]  # Ambil baris pertama
                    print(f"\n=== Validator Information ===")
                    print(f"Validator Full Name: {validator_info['full_name']}")
                    print(f"Instancy: {validator_info['instancy']}")
                    print(f"Academic Position: {validator_info['academic_position']}")

                    # Gabungkan URL menjadi satu list
                    profile_urls = []
                    if pd.notna(validator_info['scopus_url']):
                        profile_urls.append(validator_info['scopus_url'])
                    if pd.notna(validator_info['sinta_url']):
                        profile_urls.append(validator_info['sinta_url'])
                    if pd.notna(validator_info['google_scholar_url']):
                        profile_urls.append(validator_info['google_scholar_url'])

                    # Tampilkan Profile Validator
                    if profile_urls:
                        print("Profile Validator:")
                        for url in profile_urls:
                            print(f"- {url}")  # Tampilkan URL
                    else:
                        print("No profile URLs available for this validator.")
                else:
                    print("No validator information found.")
            else:
                print("This report has not been assigned to a validator.")

        except FileNotFoundError:
            print("Report data file not found.")
        except Exception as e:
            print(f"Error: {e}")