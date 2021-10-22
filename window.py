import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
class Window():
    def __init__(self):
        if os.name == "posix":
            #running on Linux
            self.display = Display(visible=0,size=(1500,1000))
            self.display.start()
            
            self.driver = webdriver.Chrome()
        else:
            #running on Windows
            options = Options()
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=options)
    def close(self):
        self.driver.quit()
        if os.name == "posix":
            self.display.stop()
        
