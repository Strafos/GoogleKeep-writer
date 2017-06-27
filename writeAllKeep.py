from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

#Google acc info
usr = '' 
pw = ''

#Log in to google account
print('Logging into account`')
driver = webdriver.Chrome()
driver.get('https://www.keep.google.com')
time.sleep(.5)
elem = driver.find_element_by_id('identifierId')
elem.send_keys(usr)
driver.find_element_by_class_name('RveJvd').click()
time.sleep(.5)
elem = driver.find_element_by_name('password')
elem.send_keys(pw)
driver.find_element_by_class_name('RveJvd').click()

time.sleep(5)
driver.find_element_by_xpath('//*[@id="gb"]/div[2]/div[2]/div[3]/div[2]').click() #Switch from Grid to List view

#Scroll to bottom to load all notes
print('Loading all notes')
time.sleep(3)
ele = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div/div[3]/div[2]/div[1]/div[7]').click()
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount==lenOfPage:
        match=True

#Get text of every note
print('Getting note text')
divs = driver.find_elements_by_css_selector('div')
all_divs = []
for div in divs:
    if "notranslate" in div.get_attribute("class") and len(div.text.encode('utf-8')) > 0:
        all_divs.append(div)
        b = div.text.encode('utf-8')

del all_divs[0]
all_test = []
for i in all_divs:
    all_test.append(i.text.encode('utf-8')) 

#Write notes to a newly made google doc
print('Writing notes to new google doc')
driver.get('https://docs.google.com/document/create')
actions = ActionChains(driver)
for test in all_test:
    actions.send_keys(test)
    actions.send_keys(Keys.ENTER)
    actions.send_keys(Keys.ENTER)
actions.perform()

elem = driver.find_element_by_css_selector('#docs-title-widget > input')
elem.send_keys('Google Keep notes')


time.sleep(20)

driver.quit()