from selenium import webdriver
import time
import sys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome('C:/Users/admin/Desktop/HotSong/chromedriver', chrome_options=chrome_options)

for i in driver.window_handles :
    try :
        driver.switch_to.window(i)
        driver.find_element_by_xpath("//*[@id=\"fp-audio\"]/div/div[1]/div[3]/div[2]/a").send_keys('\n')
        time.sleep(19)
        driver.find_element_by_xpath("//*[@id=\"fp-audio\"]/div/div[1]/div[3]/div[2]/a").send_keys('\n')
    except :
        pass

driver.quit()