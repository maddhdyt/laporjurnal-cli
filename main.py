from app.controllers.auth_controller import AuthController
from app.controllers.report_controller import ReportController
from app.views.menu_view import show_main_menu, show_admin_menu, show_user_menu, show_validator_menu

def clear_screen():
    import os
    os.system("cls" if os.name == "nt" else "clear")

def admin_menu(auth):
    """Menu khusus untuk admin."""
    while True:
        clear_screen()
        show_admin_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            clear_screen()
            auth.register_validator()
            input("\nPress Enter to return to the admin menu...")
        elif choice == "2":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to try again...")

def user_menu(auth, report_controller):
    """Menu khusus untuk user."""
    while True:
        clear_screen()
        show_user_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            clear_screen()
            user_id = auth.get_current_user_id()
            report_controller.report_journal(user_id)
            input("\nPress Enter to return to the user menu...")
        elif choice == "2":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to try again...")

def validator_menu(report_controller):
    """Menu khusus untuk validator."""
    while True:
        clear_screen()
        show_validator_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            clear_screen()
            report_controller.list_reports(status="Pending")
            input("\nPress Enter to return to the validator menu...")
        elif choice == "2":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to try again...")

def main():
    """Entry point untuk aplikasi."""
    auth = AuthController()
    report_controller = ReportController()

    while True:
        clear_screen()
        show_main_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            clear_screen()
            role = auth.login()
            if role == "admin":
                admin_menu(auth)
            elif role == "user":
                user_menu(auth, report_controller)
            elif role == "validator":
                validator_menu(report_controller)
        elif choice == "2":
            clear_screen()
            auth.register_user()
            input("\nPress Enter to return to the main menu...")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to try again...")

if __name__ == "__main__":
    main()
