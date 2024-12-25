from app.controllers.auth_controller import AuthController
from app.controllers.report_controller import ReportController
from app.views.auth_view import show_main_menu, show_user_menu, show_validator_menu, show_admin_menu
import os

def clear_screen():
    """Membersihkan layar."""
    os.system("cls" if os.name == "nt" else "clear")

def user_menu(auth, report_controller):
    """Menu untuk user."""
    while True:
        clear_screen()
        print("\n=== User Menu ===")
        print("1. Report Journal")
        print("2. Track Reports")
        print("3. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            user_id = auth.get_current_user_id()
            full_name = auth.current_user["full_name"]
            report_controller.report_journal(user_id, full_name)
            input("\nPress Enter to return to the user menu...")
        elif choice == "2":
            user_id = auth.get_current_user_id()
            report_controller.track_reports(user_id)
            input("\nPress Enter to return to the user menu...")
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

def validator_menu():
    """Menu khusus untuk validator."""
    while True:
        clear_screen()
        show_validator_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            clear_screen()
            print("Validator reviewing feature...")
            input("\nPress Enter to return to the Validator Menu...")
        elif choice == "2":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")
            input("\nPress Enter to try again...")

def admin_menu(auth):
    """Menu untuk admin."""
    while True:
        clear_screen()
        print("\n=== Admin Menu ===")
        print("1. Register Validator")
        print("2. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            auth.register_validator()
            input("\nPress Enter to return to the admin menu...")
        elif choice == "2":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

def main():
    auth = AuthController()
    report_controller = ReportController("database/tb_report.csv")

    while True:
        clear_screen()
        show_main_menu()
        choice = input("Choose an option: ")

        if choice == "1": # Login
            clear_screen()
            role = auth.login()
            if role == "user":
                user_menu(auth, report_controller)
            elif role == "validator":
                validator_menu()
            elif role == "admin":
                admin_menu(auth)
        elif choice == "2":  # Register User
            auth.register_user()
            input("\nPress Enter to return to the main menu...")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
            input("\nPress Enter to try again...")

if __name__ == "__main__":
    main()
