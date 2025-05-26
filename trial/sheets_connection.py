import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file(r"F:\College\Placements\maintenance-log-report\trial\credentials.json",scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1PJeDjik5m6m9twgUP9n9SCgMrLiH4Se3UvyFzFvLd7A"

sheet = client.open_by_key(sheet_id

values_list = sheet.sheet1.row_values(1)
print(values_list)

