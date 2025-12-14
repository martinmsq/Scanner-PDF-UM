import pdfplumber
import re
from datetime import datetime


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
            if (new_date - today).days == 17:
                print(period + " Vencimiento: "+ str(expiration) + " Fecha: " + date + " Importe:" + amount + " a una semana de vencer...")
            expiration += 1


def main():
    path = "document.pdf"
    check_date(path)


if __name__ == "__main__":
    main()
