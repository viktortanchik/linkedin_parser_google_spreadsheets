import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys

#############################
from sheets import find_url,add_new_row
from config import username,password,URL
#############################
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
#chrome_options.add_argument("--user-data-dir=./User_Data")
if sys.platform == "win32":
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--user-data-dir=C:/Temp/ChromeProfile")
    chrome_options.add_argument('--disable-infobars')
else:
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--user-data-dir=./User_Data")

#driver = webdriver.Chrome()

driver = webdriver.Chrome(
    ChromeDriverManager().install(),
    options=chrome_options
    #options=self.chrome_options,
)
#driver.set_window_size(800, 3000)

driver.maximize_window()
handles = driver.window_handles
for _, handle in enumerate(handles):
    if handle != driver.current_window_handle:
        driver.switch_to.window(handle)
        driver.close()


timeout = 5

wait = WebDriverWait(driver, 10)
driver.implicitly_wait(10)

driver.get('https://www.linkedin.com/checkpoint/lg/sign-in-another-account')





def main(urls):
    for u in urls:
        try:
            if find_url(u):
                try:
                    driver.get(u)
                    time.sleep(5)
                    #print(f"NEW URL>>>{u}")
                    date = time.strftime('%Y/%m/%d')
                    title = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/h1'))).text
                    company = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/span[1]/span[1]'))).text

                    try:
                        country = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/span[1]/span[2]'))).text
                    except:
                        country = ''
                    try:
                        salary = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/ul/li[1]/span/a'))).text
                    except:
                        salary = ''

                    try:
                        applicants = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/span[2]/span[2]/span'))).text
                    except:
                        applicants = ''
                    try:
                        job_type = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/ul/li[1]/span'))).text
                    except:
                        job_type = ''

                    try:
                        logo_url =WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/a/img'))).get_attribute('src')
                        #print(f'logo_url>>{logo_url}')
                    except:
                        logo_url = ''
                    try:
                        #print('TEST 1')
                        #time.sleep(999)
                        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/footer/button'))).click()
                        time.sleep(2)
                        #job_desc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/article/div/div[1]/span'))).text
                        job_desc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/article/div/div[1]/span'))).get_attribute('innerHTML')
                        #print('TEST 1 end',job_desc)

                    except:
                        try:#'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[4]/footer/button'
                            #print('TEST 2')

                            WebDriverWait(driver, timeout).until(EC.presence_of_element_located(
                                (By.XPATH, '/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[4]/footer/button'))).click()
                            time.sleep(2)

                            job_desc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[4]/article/div/div[1]/span'))).get_attribute('innerHTML')
                            #print('TEST 2',job_desc)
                        except:
                            job_desc = ''
                    try:#
                        contract = driver.find_element(by=By.XPATH,
                                                       value='/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/ul/li[1]/span')
                        contract = contract.text
                        contract = contract[contract.find('·') + 1:]
                    except:
                        contract = ''


                    url = u
                    index_1 = u.find('/view/') + 6
                    index_2 = u.find('/?e')
                    id = u[index_1:index_2]
                    # print(f'id--->>{id}')
                    element_id = id

                    add_new_row(date, title, company, country, salary, applicants, job_type,contract, url, logo_url, job_desc, element_id)
                except Exception as er:
                    print(f'ERROR>> URL {u} \nERROR+++>>{er}')
                    #input('ENTER')
        except:
            pass

try:
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'//*[@id="username"]'))).send_keys(username)
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'//*[@id="password"]'))).send_keys(password)
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,'//*[@id="organic-div"]/form/div[3]/button'))).click()
    #time.sleep(3)
    input('If the login was successful, press ENTER')
except:
    pass
driver.get(URL)
urls = []

pages=1
#34
def find_pages(pages):
    element1 = driver.find_element(By.XPATH, '//*[@id="main"]/div/section[1]/div')
    driver.execute_script("arguments[0].scrollBy(0, 1000);", element1)
    time.sleep(1)
    driver.execute_script("arguments[0].scrollBy(0, 1000);", element1)
    time.sleep(1)
    driver.execute_script("arguments[0].scrollBy(0, 1000);", element1)
    time.sleep(1)
    driver.execute_script("arguments[0].scrollBy(0, 1000);", element1)
    time.sleep(1)
    elem = driver.find_elements(by=By.XPATH,value='//*[@class="artdeco-pagination__indicator artdeco-pagination__indicator--number ember-view"]')
    #elem = driver.find_elements(by=By.XPATH,value='//*[@class="scaffold-layout__list-container"]')
    ''
    print(len(elem))
    try:
        if int(elem[-1].text) <pages:
            #print('ENR find urls')
            return True
    except:
        pass
    if pages==9 and len(elem)>8:
        elem[-2].click()
        #print('PAGE ...')
        #print(elems.text)
        pages = pages + 1
        elements = driver.find_elements(by=By.XPATH,
                                        value='//*[@class="disabled ember-view job-card-container__link job-card-list__title"]')
        for element in elements:
            try:
                #print(f"URL===>{element.get_attribute('href')}")
                urls.append(element.get_attribute('href'))
            except:
                print('ERROR')
        #print(f'LEN===>>{len(urls)}')
        #elems.click()
        find_pages(pages)
    else:
        try:
            elems = driver.find_element(by=By.XPATH,value=f'//*[@data-test-pagination-page-btn="{pages}"]')
            #print('pages ',pages)
            elements = driver.find_elements(by=By.XPATH,value='//*[@class="disabled ember-view job-card-container__link job-card-list__title"]')
            for element in elements:
                try:
                    urls.append(element.get_attribute('href'))
                except:
                    print('ERROR')
            #print(f'LEN===>>{len(urls)}')
            pages = pages + 1
            elems.click()
            find_pages(pages)
        except:
            print('1 pages')
            elements = driver.find_elements(by=By.XPATH,value='//*[@class="disabled ember-view job-card-container__link job-card-list__title"]')
            for element in elements:
                try:
                    urls.append(element.get_attribute('href'))
                except:
                    print('ERROR')


time.sleep(3)
find_pages(pages)
#print(len(urls))
#print(urls[-1])
main(urls)



input('END')

