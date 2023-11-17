import json
from google.auth import exceptions
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import gspread

def load_credentials():
    try:
        creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
        return creds
    except exceptions.DefaultCredentialsError:
        print("Error loading credentials.")
        return None

def connect_to_google_sheets(creds):
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
    return gspread.authorize(creds)

def clear_worksheet_except_header(worksheet):
    # Baca semua data dari worksheet
    data = worksheet.get_all_values()

    # Simpan header (baris pertama)
    header = data[0]

    # Hapus semua baris selain header
    worksheet.clear()

    # Tambahkan kembali header sebagai satu-satunya baris
    worksheet.update('A1', header)

def clear_all_worksheets_except_header(spreadsheet):
    # Ambil daftar semua lembar kerja dalam spreadsheet
    worksheets = spreadsheet.worksheets()

    for worksheet in worksheets:
        print(f"Clearing worksheet: {worksheet.title}")
        clear_worksheet_except_header(worksheet)

def main():
    # Load credentials
    credentials = load_credentials()

    if credentials:
        # Connect to Google Sheets
        client = connect_to_google_sheets(credentials)

        # Your existing code for Google Sheets operations
        spreadsheet_name = 'Qontak Data'

        spreadsheet = client.open(spreadsheet_name)

        # Clear all worksheets except the header
        clear_all_worksheets_except_header(spreadsheet)

        print("Google Sheets operations completed successfully.")

if __name__ == "__main__":
    main()