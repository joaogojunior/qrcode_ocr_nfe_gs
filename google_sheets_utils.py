import gspread
from oauth2client.service_account import ServiceAccountCredentials

import opcoes_utils

# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]


def get_client():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(opcoes_utils.le_opcao("GS_CREDENCIAL"), scope)
    return gspread.authorize(credentials)


def open_sheet(client, key=opcoes_utils.le_opcao("GS_URL_KEY")):
    return client.open_by_key(key).sheet1


def write_sheet(sheet, interval, lista_valores):
    sheet.update(interval, lista_valores)


def read_cell(sheet, cell):
    return sheet.acell(cell).value


def read_all_values(sheet):
    return sheet.get_all_values()


def next_available_row(worksheet):
    str_list = worksheet.col_values(1)
    return str(len(str_list)+1)

# print(read_all_values(sheet))
