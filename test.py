from selenium import webdriver
from pyvirtualdisplay import Display
display = Display(visible=0,size=(1500,1000))
display.start()
driver = webdriver.Chrome()
driver.get("https://www.google.com/")
print(driver.title)
driver.quit()
display.stop()
