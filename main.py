import pdfplumber
import re
import io
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'
ID_ARCHIVO_DRIVE = '12cJGuHveP0MXAaLTJZg64HoiDK8pH_jw'

def extract_pdf():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    request = service.files().get_media(fileId=ID_ARCHIVO_DRIVE)
    local_file = io.BytesIO()
    downloader = MediaIoBaseDownload(local_file, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()

    local_file.seek(0)
    service.close()
    return local_file

def extract_dates(path):
    pattern_period = r"Período:\s*(\d{1,2}/\d{4})"
    pattern_expiration = r"(Primer|Segundo|Tercer) Vencimiento:\s*(\d{2}/\d{2}/\d{4})"
    pattern_amount = r"Importe:\s*(\d+\.\d{2})"
    period = {}
    with (pdfplumber.open(path) as pdf):
        first_page = pdf.pages[0].extract_text()
        for line in first_page.splitlines():
            match_period = re.search(pattern_period, line)
            if match_period:
                period[match_period.group(0)] = []

            match_expiration = re.search(pattern_expiration, line)
            match_amount = re.search(pattern_amount, line)
            if match_expiration and match_amount:
                next_key = next(reversed(period))
                period[next_key].append(
                    (match_expiration.group(2),
                     match_amount.group(1))
                )
        return period


def check_date(path):
    today = datetime.now().date()
    for period, date_amount in extract_dates(path).items():
        expiration = 1
        for date, amount in date_amount:
            new_date = datetime.strptime(date, "%d/%m/%Y").date()
            if (new_date - today).days == 7:
                print(period + " Vencimiento: "+ str(expiration) + " Fecha: " + date + " Importe:" + amount + " a una semana de vencer...")
            expiration += 1


def main():
    file = extract_pdf()
    check_date(file)

if __name__ == "__main__":
    main()
