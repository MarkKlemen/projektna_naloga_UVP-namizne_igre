from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("https://boardgamegeek.com/browse/boardgame/page/1")

time.sleep(5)
for i in range(20):
    gumb = driver.find_element(By.CSS_SELECTOR, "a[title='next page']")
    gumb.send_keys(Keys.RETURN)
    time.sleep(5)