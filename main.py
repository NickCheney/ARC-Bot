from bs4 import BeautifulSoup
from selenium import webdriver

DRIVER_PATH="C:/Users/niche/Downloads/chromedriver_win32/chromedriver"


#set driver options
CHROME_OPTIONS = webdriver.chrome.options.Options()
'''Add to prevent graphical browswer display
chrome_options.add_argument("--headless")'''


def main():
    driver = webdriver.Chrome(DRIVER_PATH, options = CHROME_OPTIONS)
    try: 
        #get first page
        driver.get("https://getactive.gogaelsgo.com")
        driver.find_element_by_id('loginLink').click()
        driver.find_element_by_xpath('//*[@id="divLoginOptions"]/div[2]/div[2]/div/button').click()
        driver.find_element_by_id('username').send_keys('16nrc2')
        driver.find_element_by_id('password').send_keys('RyanChen3y*')
        driver.find_element_by_xpath('//*[@id="qw-region-content-inner"]/div/form/div[3]/button').click()
        driver.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div[1]/div[1]/a').click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        reserve_type = ['Squat Racks', 'Free Weights']

        for t in reserve_type:
            areas = driver.find_elements_by_xpath("//*[contains(text(), {0})]".format(t))
            #try and book an area asap
            for a in areas:
                a.click()
    except:
        print("Program failed!")
        
    driver.quit()

if __name__ == "__main__":
    main()
        
