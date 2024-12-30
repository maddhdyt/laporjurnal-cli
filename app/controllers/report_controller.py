import pandas as pd
from datetime import datetime
from tabulate import tabulate

class ReportController:
    def __init__(self, report_file):
        self.report_file = report_file
        self.validator_file = "database/tb_validator.csv"

    def report_journal(self, user_id, full_name):
        """Fitur melaporkan jurnal."""
        print("\n=== Report Journal ===")

        # Input apakah ingin melapor sebagai anonim
        while True:
            is_anonymous_input = input("Do you want to report as anonymous? (Y/N): ").strip().lower()
            if is_anonymous_input == "y":
                is_anonymous = True
                reporter_name = "Anonymous"
                break
            elif is_anonymous_input == "n":
                is_anonymous = False
                reporter_name = full_name
                break
            else:
                print("Invalid choice. Please enter Y or N.")

        # Input nama jurnal
        journal_name = input("Enter journal name: ").strip()

        # Input URL jurnal
        while True:
            journal_url = input("Enter journal URL: ").strip()
            if journal_url.startswith("http"):
                break
            else:
                print("Invalid URL. Please enter a valid URL starting with 'http'.")

        # Input alasan laporan
        reason = input("Enter your reason for reporting: ").strip()

        # Baca file CSV
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

        # Simpan kembali ke file CSV
        report_data.to_csv(self.report_file, index=False)

        # Tampilkan laporan tanpa kolom is_anonymous
        print("\nReport submitted successfully!")
        print("\n=== Submitted Report ===")
        display_report = {key: value for key, value in new_report.items() if key != "is_anonymous"}  # Exclude is_anonymous
        print(tabulate([display_report.values()], headers=display_report.keys(), tablefmt="grid"))

    def track_reports(self, user_id):
        """Menampilkan laporan yang telah dibuat oleh pengguna."""
        print("\n=== Tracking Reports ===")
        try:
            # Membaca data laporan
            report_data = pd.read_csv(self.report_file)

            # Filter laporan berdasarkan user_id
            user_reports = report_data[report_data["user_id"] == user_id]

            if user_reports.empty:
                print("You have no reports to track.")
                input("\nPress Enter to return to the User Menu...")
                return

            # Tampilkan laporan dalam bentuk tabel
            from tabulate import tabulate
            display_data = user_reports[[
                "report_id", "journal_name", "status_laporan", "tanggal_laporan"
            ]]
            print(tabulate(display_data, headers="keys", tablefmt="grid"))

            # Memilih laporan untuk melihat detail atau kembali
            report_id = input("\nEnter Report ID to view details or 0 to return: ").strip()
            if report_id == "0":
                return

            try:
                report_id = int(report_id)
            except ValueError:
                print("Invalid Report ID. Please try again.")
                return

            if report_id in user_reports["report_id"].values:
                # Call view_report_details with the correct arguments
                selected_report = user_reports[user_reports["report_id"] == report_id].iloc[0].to_dict()
                self.view_report_details(selected_report)
            else:
                print("Invalid Report ID. Please try again.")

        except FileNotFoundError:
            print("No report data file found.")
            input("\nPress Enter to return to the User Menu...")
        except Exception as e:
            print(f"Error: {e}")
            input("\nPress Enter to return to the User Menu...")

    def view_report_details(self, report):
        """Menampilkan detail laporan berdasarkan Report ID, termasuk informasi validator."""
        print("\n=== Report Details ===")
        try:
            # Display basic report details
            print(f"Report ID: {report['report_id']}")
            print(f"Journal Name: {report['journal_name']}")
            print(f"Journal URL: {report['journal_url']}")
            print(f"Reason: {report['reason']}")
            print(f"Status Laporan: {report['status_laporan']}")
            print(f"Status Jurnal: {report['status_jurnal'] if not pd.isna(report['status_jurnal']) else 'N/A'}")
            print(f"Feedback: {report['feedback'] if not pd.isna(report['feedback']) else 'N/A'}")
            print(f"Date Submitted: {report['tanggal_laporan']}")

            # Check if the report has been assigned to a validator
            if not pd.isna(report["validator_id"]):
                # Read validator data
                validator_data = pd.read_csv("database/tb_validator.csv")

                # Find the validator
                validator = validator_data[validator_data["validator_id"] == int(report["validator_id"])]
                if not validator.empty:
                    validator = validator.iloc[0]  # Get the first match
                    print("\n=== Validator Information ===")
                    print(f"Validator Name: {validator['full_name']}")
                    print(f"Validator Email: {validator['email']}")
                    print(f"Validator Institution: {validator['instancy']}")
                    print(f"Validator Position: {validator['academic_position']}")
                else:
                    print("\nNo validator information found.")
            else:
                print("\nThis report has not been assigned to a validator.")

        except Exception as e:
            print(f"Error: {e}")

    def list_pending_reports(self, validator_id):
        """Menampilkan daftar laporan dengan status 'pending'."""
        print("\n=== Pending Reports ===")
        try:
            # Membaca data laporan
            report_data = pd.read_csv(self.report_file)

            # Konversi validator_id ke string untuk konsistensi
            report_data["validator_id"] = report_data["validator_id"].fillna("").astype(str)
            report_data["status_laporan"] = report_data["status_laporan"].fillna("")

            # Filter laporan dengan status 'pending'
            pending_reports = report_data[report_data["status_laporan"] == "pending"]

            if pending_reports.empty:
                print("No pending reports available.")
                return

            # Tampilkan laporan dalam bentuk tabel
            from tabulate import tabulate
            display_data = pending_reports[[
                "report_id", "tanggal_laporan", "journal_name", "journal_url"
            ]]
            print(tabulate(display_data, headers="keys", tablefmt="grid"))

            # Memilih laporan untuk melihat detail atau menerima
            report_id = input("\nEnter Report ID to view details, accept, or 0 to return: ").strip()
            if report_id == "0":
                return

            try:
                report_id = int(report_id)
            except ValueError:
                print("Invalid Report ID. Please try again.")
                return

            if report_id in pending_reports["report_id"].values:
                selected_report = pending_reports[pending_reports["report_id"] == report_id].iloc[0].to_dict()
                self.manage_pending_report(selected_report, validator_id)
            else:
                print("Invalid Report ID. Please try again.")

        except Exception as e:
            print(f"Error: {e}")

    def view_pending_report_details(self, report_id, validator_id):
        """Menampilkan detail laporan pending dan memberikan opsi untuk menerima laporan."""
        print("\n=== Pending Report Details ===")

        try:
            # Baca data laporan
            report_data = pd.read_csv(self.report_file)

            # Filter laporan berdasarkan report_id
            report = report_data[report_data["report_id"] == report_id]

            if report.empty:
                print("Report not found.")
                return

            # Ambil informasi laporan
            report = report.iloc[0]

            # Tentukan nama pelapor berdasarkan is_anonymous
            reporter_name = "Anonymous" if report["is_anonymous"] else report["full_name"]

            print(f"Report ID: {report['report_id']}")
            print(f"Reporter Name: {reporter_name}")
            print(f"Journal Name: {report['journal_name']}")
            print(f"Journal URL: {report['journal_url']}")
            print(f"Reason: {report['reason']}")
            print(f"Date Submitted: {report['tanggal_laporan']}")

            # Opsi untuk menerima laporan
            choice = input("\nDo you want to accept this report for review? (Y/N): ").strip().lower()
            if choice == "y":
                # Pastikan kolom validator_id bertipe string
                report_data["validator_id"] = report_data["validator_id"].fillna("").astype(str)

                # Perbarui status laporan
                report_data.loc[report_data["report_id"] == report_id, "status_laporan"] = "review"
                report_data.loc[report_data["report_id"] == report_id, "validator_id"] = str(validator_id)
                report_data.to_csv(self.report_file, index=False)
                print(f"Report ID {report_id} has been accepted for review.")
            else:
                print("Report was not accepted.")

        except FileNotFoundError:
            print("No report data found.")
        except Exception as e:
            print(f"Error: {e}")
    
    def list_accepted_reports(self, validator_id):
        """Menampilkan daftar laporan yang telah diterima validator."""
        print("\n=== Accepted Reports ===")
        try:
            # Membaca data laporan
            report_data = pd.read_csv(self.report_file)

            # Konversi validator_id ke string untuk konsistensi
            report_data["validator_id"] = report_data["validator_id"].fillna("").apply(
                lambda x: str(int(x)) if x != "" else ""
            )
            report_data["status_laporan"] = report_data["status_laporan"].fillna("")

            # Filter laporan yang diterima validator
            accepted_reports = report_data[
                (report_data["validator_id"] == str(validator_id)) &
                (report_data["status_laporan"].isin(["review", "done"]))
            ]

            if accepted_reports.empty:
                # Handle empty accepted reports
                print("You have no accepted reports.")
                print("This page will remain available for future reports.")
                input("\nPress Enter to return to the Validator Menu...")
                return

            # Tampilkan laporan dalam bentuk tabel
            from tabulate import tabulate
            display_data = accepted_reports[[
                "report_id", "journal_name", "status_laporan", "tanggal_laporan"
            ]]
            print(tabulate(display_data, headers="keys", tablefmt="grid"))

            # Opsi untuk melihat detail laporan
            report_id = input("\nEnter Report ID to manage or 0 to return: ").strip()
            if report_id == "0":
                return

            try:
                report_id = int(report_id)
            except ValueError:
                print("Invalid Report ID. Please try again.")
                return

            # Place the snippet here to validate and manage the report
            if report_id in accepted_reports["report_id"].values:
                # Select the report and call manage_report
                selected_report = accepted_reports[accepted_reports["report_id"] == report_id].iloc[0].to_dict()
                self.manage_report(selected_report)  # Call manage_report with the selected report
            else:
                print("Invalid Report ID. Please try again.")

        except FileNotFoundError:
            print("No report data file found.")
            input("\nPress Enter to return to the Validator Menu...")
        except Exception as e:
            print(f"Error: {e}")
            input("\nPress Enter to return to the Validator Menu...")

    def manage_pending_report(self, report, validator_id):
        """Mengelola laporan yang berstatus pending."""
        print("\n=== Pending Report Details ===")
        print(f"Report ID: {report['report_id']}")
        print(f"Reporter Name: {report['full_name'] if not report['is_anonymous'] else 'Anonymous'}")
        print(f"Journal Name: {report['journal_name']}")
        print(f"Journal URL: {report['journal_url']}")
        print(f"Reason: {report['reason']}")
        print(f"Status Laporan: {report['status_laporan']}")
        print(f"Status Jurnal: {report['status_jurnal'] if not pd.isna(report['status_jurnal']) else 'N/A'}")
        print(f"Feedback: {report['feedback'] if not pd.isna(report['feedback']) else 'N/A'}")
        print(f"Date Submitted: {report['tanggal_laporan']}")

        print("\nOptions:")
        print("1. Accept this report for review")
        print("2. Return to Pending Reports")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            self.accept_report(report, validator_id)
        elif choice == "2":
            return
        else:
            print("Invalid choice. Returning to Pending Reports.")

    def manage_report(self, report):
        """Fungsi untuk mengelola laporan yang diterima validator."""
        while True:
            # Refresh data laporan
            report_data = pd.read_csv(self.report_file)
            updated_report = report_data[report_data["report_id"] == report["report_id"]].iloc[0].to_dict()

            print("\n=== Manage Report ===")
            print(f"Report ID: {updated_report['report_id']}")
            print(f"Reporter Name: {updated_report['full_name'] if not updated_report['is_anonymous'] else 'Anonymous'}")
            print(f"Journal Name: {updated_report['journal_name']}")
            print(f"Journal URL: {updated_report['journal_url']}")
            print(f"Reason: {updated_report['reason']}")
            print(f"Status Laporan: {updated_report['status_laporan']}")
            print(f"Status Jurnal: {updated_report['status_jurnal'] if not pd.isna(updated_report['status_jurnal']) else 'N/A'}")
            print(f"Feedback: {updated_report['feedback'] if not pd.isna(updated_report['feedback']) else 'N/A'}")
            print(f"Date Submitted: {updated_report['tanggal_laporan']}")

            print("\nOptions:")
            print("1. Validate Report")
            print("2. Mark as Pending")
            print("3. Return to Accepted Reports")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.validate_report(updated_report)
                return  # Kembali ke Accepted Reports setelah validasi selesai
            elif choice == "3":
                self.mark_as_pending(updated_report)
                return  # Kembali ke Accepted Reports setelah menandai sebagai pending
            elif choice == "4":
                break  # Kembali ke halaman Accepted Reports
            else:
                print("Invalid choice. Please try again.")

    def validate_report(self, report):
        """Validasi laporan dengan mengupdate status jurnal dan feedback, lalu menandai sebagai done."""
        print("\n=== Validate Report ===")

        # Update status jurnal
        print("Options: aman, predator, clone")
        new_status = input("Enter new journal status: ").strip().lower()
        if new_status not in ["aman", "predator", "clone"]:
            print("Invalid status. Please choose from aman, predator, or clone.")
            return

        # Tambahkan feedback
        new_feedback = input("Enter your feedback: ").strip()

        try:
            # Baca data laporan
            report_data = pd.read_csv(self.report_file)

            # Update status_jurnal, feedback, dan status_laporan
            report_data.loc[report_data["report_id"] == report["report_id"], "status_jurnal"] = new_status
            report_data.loc[report_data["report_id"] == report["report_id"], "feedback"] = new_feedback
            report_data.loc[report_data["report_id"] == report["report_id"], "status_laporan"] = "done"

            # Simpan perubahan ke file CSV
            report_data.to_csv(self.report_file, index=False)
            print("Report validated successfully. The status has been updated to 'done'.")

            # Tambahkan konfirmasi sebelum kembali
            input("\nPress Enter to return to the Accepted Reports...")
        except Exception as e:
            print(f"Error: {e}")

    def mark_as_pending(self, report):
        """Mengembalikan laporan ke status pending."""
        print("\n=== Mark as Pending ===")
        confirm = input("Are you sure you want to mark this report as pending? (Y/N): ").strip().lower()

        if confirm != "y":
            print("Operation canceled.")
            return

        try:
            # Baca data laporan
            report_data = pd.read_csv(self.report_file)

            # Update status_laporan dan hapus validator_id
            report_data.loc[report_data["report_id"] == report["report_id"], "status_laporan"] = "pending"
            report_data.loc[report_data["report_id"] == report["report_id"], "validator_id"] = None
            report_data.to_csv(self.report_file, index=False)

            print("Report marked as pending.")
            input("\nPress Enter to return to the Validator Menu...")
            raise StopIteration  # Digunakan untuk keluar dari loop manage_report

        except StopIteration:
            return  # Kembali langsung ke Validator Menu
        except Exception as e:
            print(f"Error: {e}")

    def accept_report(self, report, validator_id):
        """Menerima laporan untuk direview oleh validator."""
        print("\n=== Accept Report ===")
        try:
            # Baca data laporan
            report_data = pd.read_csv(self.report_file)

            # Update validator_id dan status_laporan
            report_data.loc[report_data["report_id"] == report["report_id"], "validator_id"] = validator_id
            report_data.loc[report_data["report_id"] == report["report_id"], "status_laporan"] = "review"

            # Simpan kembali ke file CSV
            report_data.to_csv(self.report_file, index=False)
            print(f"Report ID {report['report_id']} has been accepted for review.")
        except Exception as e:
            print(f"Error: {e}")
