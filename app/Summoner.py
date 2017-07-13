from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import clipboard

driver = webdriver.Chrome('/Users/dliang/Desktop/chromedriver')

def url_open(username):
    driver.get("https://na.op.gg/summoner/userName=" + str(username))

def get_info():
    info = []
    info.append(driver.find_element_by_class_name("tierRank").text)
    LP = int(driver.find_element_by_class_name("LeaguePoints").text.split()[0])
    info.append(LP)
    info.append(driver.find_element_by_class_name("winratio").text.split()[2][:2])
    MMR_button = driver.find_element_by_css_selector(".Button.SemiRound.White")
    MMR_button.click()
    time.sleep(3)
    MMR = driver.find_element_by_xpath('//*[@id="ExtraView"]/div/div[1]/div[1]').text
    if ("ormal" in MMR):
        info.append(20)
    elif ("lower" in MMR):
        info.append(17)
    elif ("higher" in MMR):
        info.append(23)
    if LP == 100:
        info.append(True)
    else:
        info.append(False)
    return info
