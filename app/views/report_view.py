def show_list_of_reports(reports, status="Pending"):
    print(f"\n=== List of Reports (Status: {status}) ===")
    if reports.empty:
        print(f"No reports found with status: {status}.")
    else:
        print(reports.to_string(index=False))
