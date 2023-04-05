import gspread
from google.oauth2.service_account import Credentials
from config import file,SHEETS_NAME
import pprint

#print_p = pprint.PrettyPrinter()
def connect ():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_file(
        file,
        scopes=scopes
    )
    gc = gspread.authorize(credentials)
    sh = gc.open(SHEETS_NAME)

    # Get the first sheet
    wk = sh.sheet1
    return wk

connect()
#print(wk.get_all_records())
#print(print_p.pprint(wk.get_all_records()))
# for url in wk.get_all_records():
#     print(url['URL of job Application'])

def find_url(url):
    index_1=url.find('/view/') + 6
    index_2= url.find('/?e')
    #print(url[index_1:index_2])
    id = url[index_1:index_2]
    wk = connect()
    for u in wk.get_all_records():
        #print(f'ID--->>{id}   element_id--->>{u["element_id"]}')
        if int(u['element_id']) == int(id):
            #print(f'ID--->>{id}   element_id--->>{u["element_id"]}')
            return False
    return True



# Функция для добавления новой строки
def add_new_row(date, title, company, country, salary, applicants, job_type, url, logo_url, Logo,job_desc,element_id):
    wk = connect()
    new_row = [date, title, company,  country, salary, applicants, job_type, url, logo_url, Logo,job_desc,element_id]
    wk.append_row(new_row)
    print("The new row has been successfully added to the table.")

# Пример использования функции
#add_new_row("2023-03-27", "Python Developer", "Google", "Mountain View", "Santa Clara", "USA", "150000", "100", "Full-time", "https://www.google.com/careers", "https://www.google.com/logo.png", "We are looking for a Python Developer...")
