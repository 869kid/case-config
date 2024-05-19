# Case Configurator

## Overview

The Case Configurator is a tool designed to read and parse data from Google Sheets and generate configuration files in JSON format. This tool is useful for managing and configuring cases and rewards in a structured and automated manner.

## Features

- Reads data from Google Sheets
- Cleans and processes data
- Parses case and reward information
- Generates JSON configuration files

## Prerequisites

- Python 3.6 or later
- Google Cloud project with Google Sheets API and Google Drive API enabled
- `credentials.json` file from your Google Cloud project

## Installation

1. Clone the repository:
   
   git clone https://github.com/869kid/case-config.git
   cd case-config

2. Create and activate a virtual environment (optional but recommended):\
 
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install required dependencies:

  pip install -r requirements.txt

4. Place the credentials.json file in the project directory.

## Usage

1. Update the Google Sheets ID and range in the main() function if necessary:
 
    SAMPLE_SPREADSHEET_ID = 'your_google_sheets_id'

2. Run the script:
   python case-config.py
   
3. The script will read the data from the specified Google Sheets, clean and process it, and generate a JSON configuration file named case_config.json.

№№ Code Structure
    case-config.py: Main script containing all functions and logic for reading, processing, and generating configuration files.
    credentials.json: File containing OAuth 2.0 credentials for accessing Google Sheets and Google Drive APIs.
    token.pickle: File storing user's access and refresh tokens for subsequent runs.

№№ Important Notes

    Ensure that the credentials.json file is properly configured with the necessary API scopes:

{
  "installed": {
    "client_id": "your_client_id",
    "project_id": "your_project_id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your_client_secret",
    "redirect_uris": [
      "urn:ietf:wg:oauth:2.0:oob",
      "http://localhost"
    ]
  }
}


If you change the SCOPES in the script, delete the token.pickle file to reauthorize.
