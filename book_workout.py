from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display
import time as tm, datetime as dt
from datetime import date, time, datetime, timedelta
import traceback
import os

def str_to_date(date):
    return datetime.strptime(date, "%A, %B %d, %Y").date()

def in_timerange(min_start, max_end, s_start, s_end):
    s_start = datetime.strptime(s_start, "%I:%M %p").time()
    s_end = datetime.strptime(s_end, "%I:%M %p").time()

    if s_start >= min_start and s_end <= max_end:
        return True
    return False
    
def book_workout(user, order):
    #TODO: use gender flag instead of exclusions or let user set exclusions
    BASE_URL = "https://getactive.gogaelsgo.com"
    username = user.netid
    password = user.password
    reserve_types = order.areas
    excluding = []
    if user.gender == 'male':
        excluding.append("women's fitness zone")
    req_date = order.date
    times = order.times.time_ranges

    try:
        display = Display(visible=0,size=(1500,1000))
        display.start()
        driver = webdriver.Chrome()
        #get first page
        driver.get(BASE_URL)
        #accept cookies
        driver.find_element_by_xpath('//*[@id="gdpr-cookie-accept"]').click()
        driver.find_element_by_id('loginLink').click()
        login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="divLoginOptions"]/div[2]/div[2]/div/button')))
        login_button.click()
        username_entry = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'username')))
        username_entry.send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_xpath('//*[@id="qw-region-content-inner"]/div/form/div[3]/button').click()
        driver.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div[1]/div[1]/a').click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        programs = [s('div')[0] for s in soup.find(id='list-group').find_all('div',recursive=False)]
        
        #wait here until the correct time
        while datetime.now() < order.earliest_datetime() - timedelta(days=3):
            tm.sleep(1.0)
            print("on main page, waiting...")

        for t in reserve_types:
            print(f"Trying {t} as search term")
            t = t.lower()
            tprograms = [p for p in programs if (t in p.text.lower()) and not any([e in p.text.lower() for e in excluding])]
            tpaths = [p.attrs['onclick'] for p in tprograms]
            turls = [BASE_URL + l[l.index("'")+1:len(l)-1] for l in tpaths]
            for url in turls:
                #check new area
                driver.get(url)

                area_title = driver.find_element_by_xpath('//*[@id="mainContent"]/div[2]/nav/ol/li[2]').text
                print(f"Checking {area_title}")

                #attempt to make reservation within required timeframe on correct date
                timeslots = driver.find_elements_by_xpath('//*[@id="mainContent"]/div[2]/section/div')
                #tm.sleep(5.0)
                #print(timeslots)
                for slot in timeslots:
                    #get date for sessions timeslot
                    slot_date = str_to_date(slot.find_element_by_xpath(".//div/div/label").text)

                    #past the desired date for area
                    if slot_date > req_date:
                        print("No applicable sessions")
                        break
                    elif slot_date == req_date:
                        #print("found slot on required date!")
                        period, availability = slot.find_element_by_xpath(".//div/div/div/small").text.split('\n')
                        for avper in times:
                            #avper.print_range()
                            #print(period)
                            if in_timerange(avper.t1,avper.t2, *period.split(' - ')):
                                #print("found slot in correct time range!")
                                if availability != "No Spots Available":
                                    print("Attempting to register for",area_title,"from",period)
                                    slot.find_element_by_xpath(".//div/div/div[2]/button").click()
                                    accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'btnAccept')))
                                    # create action chain object
                                    action = ActionChains(driver)
  
                                    # perform the operation
                                    action.move_to_element(accept_button).perform()
                                    accept_button.click()
                                    
                                    #accept_button.click()
                                    #driver.find_element_by_id('btnAccept').click()
                                    driver.find_element_by_id('checkoutButton').click()
                                    card_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                                              '//*[@id="ExistingCardsModal"]/div/div/div[2]/div/div[2]/button')))
                                    card_button.click()
                                    #driver.find_element_by_xpath('//*[@id="ExistingCardsModal"]/div/div/div[2]/div/div[2]/button').click()
                                    print('Success!')
                                    driver.quit()
                                    display.stop()
                                    return True
                driver.back()
            
    except Exception as e:
        print("Error during booking session!")
        traceback.print_exc()
    
    driver.quit()
    display.stop()
    return False
