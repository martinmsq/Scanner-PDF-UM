# University checkbook date scanner.

Python script designed to monitor the expiration dates of tuition fees from the Universidad de Mendoza (UM), extracted from a PDF file stored in Google Drive. The script sends an email notification one week before a due date.

## Features

- **PDF Extraction from Google Drive**: Connects to the Google Drive API to download a specific PDF file.
- **PDF Analysis**: Uses `pdfplumber` to read the PDF content and extract expiration dates and associated amounts.
- **Email Notifications**: Sends an alert email when a payment is 7 days away from its due date.
- **Automation with GitHub Actions**: Runs automatically every day at a scheduled time thanks to a GitHub Actions workflow.
- **Credential Management**: Uses environment variables and GitHub secrets to securely manage credentials and configurations.

## How It Works

1.  **PDF Download**: The script authenticates with Google Drive using a service account and downloads the tuition fee PDF specified by its ID.
2.  **Date Extraction**: It analyzes the PDF text, searching for patterns that match billing periods, due dates, and amounts.
3.  **Date Verification**: Compares the extracted due dates with the current date.
4.  **Notification Sending**: If any of the due dates is exactly 7 days away, a message is constructed and an email is sent to the configured address.
5.  **Scheduled Execution**: A GitHub Actions workflow is responsible for running the `main.py` script every day at 8:00 AM (Argentina time).

## File Structure
Below is a detail of each important file in the project and its content.

`main.py`
It contains all the logic to download, parse the PDF, and send notifications.

`requirements.txt`
Defines the Python dependencies required for the project to work.

`.github/workflows/github-actions-cron.yml`
Defines the GitHub Actions workflow that automates the script's execution.

## Configuration
For the script to work, you need to configure the following environment variables.

### Local Development
Create a `.env` file in the root of the project with the following content:

```
SERVICE_ACCOUNT_FILE='credentials.json'
SCOPES='https://www.googleapis.com/auth/drive'
ID_ARCHIVO_DRIVE='YOUR_GOOGLE_DRIVE_FILE_ID'
EMAIL='your_email@domain.com'
PASSWORD='your_email_password'
SMTP_SERVER='smtp.your_provider.com'
SMTP_PORT=465
```

Additionally, you must obtain a `credentials.json` file from a Google Cloud service account with permissions to access the Google Drive API and place it in the project root.

### GitHub Actions

In your GitHub repository settings, you must add the following variables and secrets:

-   **Repository Variables (`vars`)**:
    -   `SCOPE`: `https://www.googleapis.com/auth/drive`
    -   `ID_ARCHIVO_DRIVE`: The ID of the file in Google Drive.
    -   `EMAIL`: Your email address.
    -   `SMTP_SERVER`: Your email provider's SMTP server.
    -   `SMTP_PORT`: The SMTP server port (usually 465 for SSL).

-   **Repository Secrets (`secrets`)**:
    -   `SERVICE_ACCOUNT_FILE`: The full content of your `credentials.json` file, encoded in Base64.
    -   `PASSWORD`: Your email password.
